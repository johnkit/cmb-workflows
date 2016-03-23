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
print 'Loading cumulusclient'

import json
import os
import sys
import time
import uuid

import requests
from girder_client import GirderClient, HttpError

class CumulusClient():
  '''Application interface to cumulus-based client for HPC systems
  supporting NEWT API.

  Note: the methods must be called in a specific order!
    create_cluster()
    create_omega3p_script()
    create_job()
    upload_inputs()
    submit_job()

  Then optionally:
    monitor_job()
    download_results()
    release_resources()
  '''
  # ---------------------------------------------------------------------
  def __init__(self, girder_url, newt_sessionid):
    '''
    '''
    self._client = None
    self._cluster_id = None
    self._girder_url = girder_url
    self._input_folder_id = None
    self._job_folder_id = None
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
    print 'private_folder_id', self._private_folder_id

  # ---------------------------------------------------------------------
  def job_id(self):
    '''Returns current job id (which may be None)
    '''
    return self._job_id

  # ---------------------------------------------------------------------
  def create_cluster(self, machine_name, cluster_name=None):
    '''
    '''
    if cluster_name is None:
      user = self._client.get('user/me')
      user_name = user.get('firstName', 'user')
      cluster_name = '%s.%s' % (machine_name, user_name)

    cluster = None
    cluster_list = self._client.get('clusters')
    for extant_cluster in cluster_list:
      if extant_cluster['name'] == cluster_name:
        cluster = extant_cluster
        self._cluster_id = extant_cluster['_id']
        break

    if not cluster:
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

    # Reset the state of the cluster
    body = {
      'status':  'created'
    }
    r = self._client.patch('clusters/%s' % self._cluster_id, data=json.dumps(body))

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
        print r
        raise Exception('ERROR creating cluster')

      if sleeps > 9:
        raise Exception('Cluster never moved into running state')
      sleeps += 1

  # ---------------------------------------------------------------------
  def create_omega3p_script(self, omega3p_filename, name=None, number_of_tasks=1):
    '''Creates script to submit omega3p job
    '''
    command = 'srun -n %s /project/projectdirs/ace3p/{{machine}}/omega3p %s' % \
      (number_of_tasks, omega3p_filename)
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
    '''DEPRECATED Uploads input files
    '''
    folder_id = self.get_folder(self._private_folder_id, folder_name)
    if folder_id is None:
      return
    print 'input_folder_id', folder_id
    self._input_folder_id = folder_id

    def upload_file(path):
      name = os.path.basename(path)
      size = os.path.getsize(path)
      with open(path, 'rb') as fp:
        self._client.uploadFile(
          self._input_folder_id, fp, name, size, parentType='folder')

    for input_path in input_paths:
      if not input_path or not os.path.exists(input_path):
        raise Exception('Input file not found: %s' % input_path)
      upload_file(input_path)

  # ---------------------------------------------------------------------
  def create_output_folder(self, folder_name='output_files'):
    '''DEPRECATED
    '''
    folder_id = self.get_folder(self._private_folder_id, folder_name)
    print 'output_folder_id', folder_id
    self._output_folder_id = folder_id

  # ---------------------------------------------------------------------
  def create_job(self, job_name, tail=None):
    '''
    '''
    # Create job folders
    folder_name = uuid.uuid4().hex  # unique name
    self._job_folder_id = self.get_folder(self._private_folder_id, folder_name)
    print 'Created job folder', folder_name
    self._input_folder_id = self.get_folder(self._job_folder_id, 'input_files')
    self._output_folder_id = self.get_folder(self._job_folder_id, 'output_files')

    # Make sure job_name isn't null
    if not job_name:
      job_name = 'CumulusJob'

    # Create job spec
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
    print 'Created job_id', self._job_id

  # ---------------------------------------------------------------------
  def upload_inputs(self, input_paths):
    '''Uploads input files to input folder
    '''
    if not self._input_folder_id:
      raise Exception('Input folder missing')

    def upload_file(path):
      name = os.path.basename(path)
      size = os.path.getsize(path)
      with open(path, 'rb') as fp:
        self._client.uploadFile(
          self._input_folder_id, fp, name, size, parentType='folder')

    for input_path in input_paths:
      if not input_path or not os.path.exists(input_path):
        raise Exception('Input file not found: %s' % input_path)
      upload_file(input_path)

  # ---------------------------------------------------------------------
  def submit_job(self,
    machine,
    project_account,
    timeout_minutes,
    queue='debug',
    qos = None,
    number_of_nodes=1,
    job_output_dir=None):
    '''
    '''
    body = {
      'machine': machine,
      'account': project_account,
      'numberOfNodes': number_of_nodes,
      'maxWallTime': {
        'hours': 0,
        'minutes': timeout_minutes,
        'seconds': 0
      },
      'queue': queue,
    }
    if qos:
      body['qualityOfService'] = qos
    if job_output_dir:
      body['jobOutputDir'] = job_output_dir
      print 'Setting jobOutputDir', job_output_dir
    url = 'clusters/%s/job/%s/submit' % (self._cluster_id, self._job_id)
    self._client.put(url, data=json.dumps(body))
    print 'Submitted job', self._job_id

  # ---------------------------------------------------------------------
  def monitor_job(self, tail=None):
    '''Periodically monitors job status
    '''
    log_offset = 0
    job_timeout = 60 * timeout_minutes
    start = time.time()
    while True:
      time.sleep(2)

      # Provide some feedback at startup
      if log_offset == 0:
        sys.stdout.write('.')

      #print 'Checking status'
      r = self._client.get('jobs/%s' % self._job_id)
      #print r

      if r['status'] in ['error', 'unexpectederror']:
        r = self._client.get('jobs/%s/log' % self._job_id)
        raise Exception(str(r))
      elif r['status'] == 'complete':
        break

      # Tail log file
      if tail:
        params = {
          'offset': log_offset,
          'path': tail
        }
        #print 'Checking tail'
        r = self._client.get('jobs/%s/output' % self._job_id, parameters=params)
        #print r
        output = r['content']

        if output and log_offset == 0:
          print  # end the user feedback dots

        log_offset += len(output)

        for l in output:
          print l

      sys.stdout.flush()

      if time.time() - start > job_timeout:
        raise Exception('Job timeout')

  # ---------------------------------------------------------------------
  def download_results(self, destination_folder):
    '''Downloads all output files to a local directory

    '''
    if not os.path.exists(destination_folder):
      os.makedirs(destination_folder)

    self._client.downloadFolderRecursive(
      self._output_folder_id, destination_folder)

    print 'Downloaded files to %s' % destination_folder

  # ---------------------------------------------------------------------
  def release_resources(self):
    '''Closes/deletes any current resources

    '''
    resource_info = {
      'clusters': [self._cluster_id],
      'jobs': [self._job_id],
      'scripts': [self._script_id],
      'folder': [self._job_folder]
    }
    for resource_type, id_list in resource_info.items():
      for resource_id in id_list:
        if resource_id is not None:
          url = '%s/%s' % (resource_type, resource_id)
          self._client.delete(url)

    self._input_folder_id = None
    self._job_folder_id = None
    self._job_id = None
    self._output_folder_id = None
    self._script_id = None

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
