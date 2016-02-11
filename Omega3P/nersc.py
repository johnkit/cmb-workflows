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
print 'Loading nersc'

import imp
import os
import sys
import traceback

import requests
import smtk

# ---------------------------------------------------------------------
def _load_local_module(module_name):
  '''Helper function to import new module or reload existing one.

  Note: module (module_name.py file) must be in *same directory* as this file.
  '''
  abs_path = os.path.abspath(__file__)
  abs_dir = os.path.dirname(abs_path)
  module_args = imp.find_module(module_name, [abs_dir])
  imp.load_module(module_name, *module_args)
  return sys.modules.get(module_name)


# Explicitly load local modules, to pick up any mods
cumulusclient = _load_local_module('cumulusclient')
newtclient = _load_local_module('newtclient')

from cumulusclient import CumulusClient
from newtclient import NewtClient

# ---------------------------------------------------------------------
def submit_omega3p(scope, sim_item):
  '''Submits Omega3P job to NERSC via cumulus server

  This is the module entry point.
  Returns boolean indicating success.
  '''
  ok = True   # return value
  scope.cumulus = None
  scope.nersc = None

  sim_item = smtk.attribute.to_concrete(sim_item)
  try:
    if not os.path.exists(scope.model_path):
      raise Exception('Cannot find model file at %s' % scope.model_path)

    if not os.path.exists(scope.output_path):
      raise Exception('Cannot find Omega3P file at %s' % scope.output_path)

    login_nersc(scope, sim_item)
    scope.cumulus = create_cumulus_client(scope, sim_item)

    raise Exception('ERROR: Submission to NERSC not yet implemented')
  except Exception as ex:
    traceback.print_exc()
    ok = False
  finally:
    release_resources(scope)

  return ok

# ---------------------------------------------------------------------
def release_resources(scope):
  '''
  '''
  print 'Releasing resources'
  if scope.cumulus:
    scope.cumulus.release_resources()

  if scope.nersc:
    scope.nersc.logout()

# ---------------------------------------------------------------------
def login_nersc(scope, sim_item):
  '''Logs into NERSC and gets session id

  '''
  scope.newt_sessionid = None

  # Check user inputs
  username = _get_string(sim_item, 'NERSCAccountName')
  #print 'username', username
  if not username:
    raise Exception('ERROR: NERSC account name not specified')

  password = _get_string(sim_item, 'NERSCAccountPassword')
  #print 'password', password
  if not password:
    raise Exception('ERROR: NERSC account password not specified')

  nersc_url = 'https://newt.nersc.gov/newt'
  scope.nersc = NewtClient(nersc_url)
  r = scope.nersc.login(username, password)
  scope.newt_sessionid = scope.nersc.get_sessionid()
  print 'newt_sessionid', scope.newt_sessionid

# ---------------------------------------------------------------------
def create_cumulus_client(scope, sim_item):
  '''Instantiates Cumulus client

  '''
  item = sim_item.find('CumulusHost')
  cumulus_item = smtk.attribute.to_concrete(item)
  cumulus_host = cumulus_item.value(0)
  if not cumulus_host:
    raise Exception('ERROR: Cumulus host not specified')

  return CumulusClient(cumulus_host, scope.newt_sessionid)

# ---------------------------------------------------------------------
def _get_string(group_item, name):
  '''Looks for StringItem contained by group.

  Returns either string or None if not found
  '''
  item = group_item.find(name)
  if not item:
    print 'WARNING: item \"%s\" not found' % name
    return None

  concrete_item = smtk.attribute.to_concrete(item)
  if concrete_item.type() != smtk.attribute.Item.STRING:
    print 'WARNING: item \"%s\" not a string item' % name
    return None

  return concrete_item.value(0)
