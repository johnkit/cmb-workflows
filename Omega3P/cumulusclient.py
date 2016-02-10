#=============================================================================
#
#  Copyright (c) Kitware, Inc.
#  All rights reserved.
#  See LICENSE.txt for details.
#
#  This software is distributed WITHOUT ANY WARRANTY; without even
#  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE.  See the above copyright notice for more information.
#
#=============================================================================

import json
import os
import time

import requests
from girder_client import GirderClient, HttpError

class CumulusClient():
  '''Application interface to cumulus-based client for HPC systems
  supporting NEWT API

  '''
  # ---------------------------------------------------------------------
  def __init__(self, girder_url, newt_sessionid):
    '''
    '''
    self._client = None
    self._cluster_id = None
    self._girder_url = girder_url
    self._input_folder_id = None
    self._job_id = None
    self._output_folder_id = None
    self._private_folder_id = None
    self._script_id = None
    self._session = requests.Session()

    # Authenticate with Girder using the newt session id
    url = '%s/api/v1/newt/authenticate/%s' % \
      (self._girder_url, newt_sessionid)
    r = self._session.put(url)
    if r.status_code != 200:
      raise HttpError(r.status_code, r.text, r.url, r.request.method)

    # Instantiate Girder client
    url = '%s/api/v1' % self._girder_url
    self._client = GirderClient(apiUrl=url)
    self._client.token = self._session.cookies['girderToken']

    user = self._client.get('user/me')
    #print 'user', user
    user_id = user['_id']
    r = self._client.listFolder(user_id, 'user', name='Private')
    if len(r) != 1:
      raise Exception('Wrong number of users; should be 1 got %s' % len(r))
    self._private_folder_id = r[0]['_id']
    print 'private folder id', self._private_folder_id

  # ---------------------------------------------------------------------
  def create_cluster(self, machine_name, cluster_name=None):
    '''
    '''
    if cluster_name is None:
      user = self._client.get('user/me')
      user_name = user.get('firstName', 'user')
      cluster_name = '%s.%s' % (machine_name, user_name)

    body = {
      'config': {
        'host': machine_name
      },
      'name': cluster_name,
      'type': 'newt'
    }

    r = self._client.post('clusters', data=json.dumps(body))
    self._cluster_id = r['_id']
    print 'cluster_id', self._cluster_id

    # Now test the connection
    r = self._client.put('clusters/%s/start' % self._cluster_id)
    sleeps = 0
    while True:
      time.sleep(1)
      r = self._client.get('clusters/%s/status' % self._cluster_id)

      if r['status'] == 'running':
        break
      elif r['status'] == 'error':
        r = self._client.get('clusters/%s/log' % self._cluster_id)
        print 'Error creating cluster'
        print r.text

      if sleeps > 9:
        raise Exception('Cluster never moved into running state')
      sleeps += 1

  # ---------------------------------------------------------------------
  def create_omega3p_script(self, omega3p_filename, name=None, number_of_nodes=1):
    '''Creates script to submit omega3p job
    '''
    command = 'srun -n %d /project/projectdirs/ace3p/{{machine}}/omega3p %s' % \
      (number_of_nodes, omega3p_filename)
    if name is None:
      name = omega3p_filename
    body = {
      'commands': [command],
      'name': name
    }
    r = self._client.post('scripts', data=json.dumps(body))
    self._script_id = r['_id']
    print 'script_id', self._script_id

  # ---------------------------------------------------------------------
  def create_input(self, input_paths, folder_name='input_files'):
    '''Uploads input files
    '''
    folder_id = self.get_folder(self._private_folder_id, folder_name)
    if folder_id is None:
      return
    print 'input_folder_id', folder_id
    self._input_folder_id = folder_id

    def upload_file(path):
      size = os.path.getsize(path)
      with open(path, 'rb') as fp:
        self._client.uploadFile(
          self._input_folder_id, fp, path, size, parentType='folder')

    for input_path in input_paths:
      if not input_path or not os.path.exists(input_path):
        raise Exception('Input file not found: %s' % input_path)
      upload_file(input_path)

  # ---------------------------------------------------------------------
  def create_output_folder(self, folder_name='output_files'):
    '''
    '''
    folder_id = self.get_folder(self._private_folder_id, folder_name)
    print 'output_folder_id', folder_id
    self._output_folder_id = folder_id

  # ---------------------------------------------------------------------
  def create_job(self, job_name='CumulusJob', tail=None):
    '''
    '''
    body = {
      'name': job_name,
      'scriptId': self._script_id,
      'output': [{
        'folderId': self._output_folder_id,
        'path': '.'
      }],
      'input': [
        {
          'folderId': self._input_folder_id,
          'path': '.'
        }
      ]
    }

    if tail:
      body['output'].append({
        "path": tail,
        "tail": True
      })

    job = self._client.post('jobs', data=json.dumps(body))
    self._job_id = job['_id']
    print 'job_id', self._job_id

  # ---------------------------------------------------------------------
  def finalize(self):
    '''Closes/deletes any current resources

    '''
    resource_info = {
      'jobs': [self._job_id],
      'scripts': [self._script_id],
      'folder': [self._input_folder_id, self._output_folder_id]
    }
    for resource_type, id_list in resource_info.items():
      for resource_id in id_list:
        url = '%s/%s' % (resource_type, resource_id)
        self._client.delete(url)

  # ---------------------------------------------------------------------
  def get_folder(self, parent_id, name):
    '''Returns folder_id, creating one if needed
    '''
    # Check if folder already exists
    folder_list = self._client.listFolder(parent_id, name=name)
    if folder_list:
      folder = folder_list[0]
      #print 'found folder %s: %s' % (name, str(folder))
      return folder['_id']

    # (else)
    try:
      r = self._client.createFolder(parent_id, name)
      return r['_id']
    except HttpError as e:
      print e.responseText

    return None
