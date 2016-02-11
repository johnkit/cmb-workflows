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
print 'Loading newtclient'

import requests

class NewtClient():
  '''Http client to servers that implement the NEWT API

  The NEWT API is a collection of REST based services designed
  for HPC computing. See https://newt.nersc.gov.

  This class is intended for use with cumulus/hpccloud library.
  As such, only the main authentication functions are implemented.
  '''

  # ---------------------------------------------------------------------
  def __init__(self, base_url):
    self._base_url = base_url
    self._session_id = None

  # ---------------------------------------------------------------------
  def get_authentication_status(self):
    '''Checks current login status

    Returns json object with authentication status
    '''
    url = '%s/login/' % self._base_url
    r = requests.get(url)
    return r.json()
    
  # ---------------------------------------------------------------------
  def login(self, username, password):
    '''Sends login command to server.

    Returns json object with authentication status
    '''
    credentials = {
      'username': username,
      'password': password
    }
    url = '%s/login/' % self._base_url
    r = requests.post(url, data=credentials)
    js = r.json()
    if not js.get('auth'):
      print 'NERSC url', url
      print 'credentials', credentials
      print 'NERSC response', r.text
      raise Exception('Login to NERSC failed')

    self._session_id = js.get('newt_sessionid')
    return r.json()

  # ---------------------------------------------------------------------
  def logout(self):
    '''Sends logout command to server.

    Returns json object with authentication status
    '''
    url = '%s/logout/' % self._base_url
    r = requests.get(url)
    self._session_id = None
    return r.json()

  # ---------------------------------------------------------------------
  def get_sessionid(self, login_response=None):
    '''Returns newt_sessionid

    If login_repsonse object passed in, will parse that.
    Otherwise returns internal value
    '''
    if login_response is not None:
      return login_response.get('newt_sessionid')
    # (else)
    return self._session_id
