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
"""
Export functions for submitting jobs to NERSC
"""

import os
import requests
import sys
import smtk

# ---------------------------------------------------------------------
def submit_omega3p(scope, sim_item):
  '''Submits Omega3P job to NERSC via cumulus server

  Returns boolean indicating success
  '''
  sim_item = smtk.attribute.to_concrete(sim_item)

  # Confirm that output and model files exist
  if not os.path.exists(scope.model_file):
    print 'Cannot find model file at %s' % scope.model_file
    return false

  if not os.path.exists(scope.output_file):
    print 'Cannot find Omega3P file at %s' % scope.output_file
    return false

  #fcn_sequence = [check_cumulus_host, check_nersc_auth]
  if not check_cumulus_host(scope, sim_item):
    return False

  if not check_nersc_auth(scope, sim_item):
    return False

  print 'ERROR: Connection to NERSC not yet implemented'
  return False

# ---------------------------------------------------------------------
def check_cumulus_host(scope, sim_item):
  '''Checks for CumulusHost item and returns True if found

  '''
  item = sim_item.find('CumulusHost')
  cumulus_item = smtk.attribute.to_concrete(item)
  if cumulus_item is None:
    print 'CumulusHost item not found'
    return False
  cumulus_host = cumulus_item.value(0)
  if not cumulus_host:
    print 'Cumulus host name missing'
    return False
  url = 'http://%s/%s' % (cumulus_host, '/api/v1/system/check?mode=basic')
  response = requests.get(url)
  print 'DEBUG: cumulus host check reponse status: %d' % response.status_code
  if response.status_code != 200:
    print 'Unable to connect to cumulus host (%s)' % url
    return False

  scope.cumulus_host = cumulus_host
  return True

# ---------------------------------------------------------------------
def check_nersc_auth(scope, sim_item):
  '''Checks for CumulusHost item and returns True if found

  '''
  # Check user inputs
  username = get_string(sim_item, 'NERSCAccountName')
  if not username:
    print 'ERROR: NERSC account name not specified'
    return False

  password = get_string(sim_item, 'NERSCAccountPassword')
  if not password:
    print 'ERROR: NERSC account password not specified'
    return False

  machine = get_string(sim_item, 'Machine')
  if not machine:
    print 'ERROR: NERSC machine not specified'
    return False

  #Todo get NERSC session id

  return True

# ---------------------------------------------------------------------
def get_string(group_item, name):
  '''Looks for StringItem contained by group.

  Returns either string or None if not found
  '''
  item = group_item.find(name)
  if not item:
    return None

  concrete_item = smtk.attribute.to_concrete(item)
  if concrete_item.type() != smtk.attribute.Item.STRING:
    return None

  return concrete_item.value(0)
