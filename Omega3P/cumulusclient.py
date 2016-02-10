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
        self.fail('Cluster never moved into running state')
      sleeps += 1

  # ---------------------------------------------------------------------
  def create_omega3p_script(self, omega3p_path, name=None, number_of_nodes=1):
    '''Creates script to submit omega3p job
    '''
    command = 'srun -n %d /project/projectdirs/ace3p/{{machine}}/omega3p %s' % \
      (number_of_nodes, omega3p_path)
    if name is None:
      name = os.path.basename(omega3p_path)
    body = {
      'commands': [command],
      'name': name
    }
    r = self._client.post('scripts', data=json.dumps(body))
    self._script_id = r['_id']
    print 'script_id', self._script_id

  # ---------------------------------------------------------------------
  def finalize(self):
    '''Closes/deletes any current resources

    '''
    if self._script_id is not None:
      url = 'scripts/%s' % self._script_id
      self._client.delete(url)

    if self._cluster_id is not None:
      url = 'clusters/%s' % self._cluster_id
      self._client.delete(url)
