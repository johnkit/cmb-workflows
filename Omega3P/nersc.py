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
import shutil

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
    # Verify input files
    check_file(scope.model_path, 'Cannot find model file at %s')
    check_file(scope.output_path, 'Cannot find Omega3P file at %s')

    # Start NERSC session
    login_nersc(scope, sim_item)

    # Initialize CumulusClient
    scope.cumulus = create_cumulus_client(scope, sim_item)

    # Create cluster
    machine = get_string(sim_item, 'Machine')
    print 'machine', machine
    if not machine:
      raise Exception('Machine name not specified')
    scope.cumulus.create_cluster(machine)

    # Create run script
    omega3p_filename = os.path.basename(scope.output_path)
    number_of_nodes = get_integer(sim_item, 'NumberOfNodes')
    if not number_of_nodes:
      number_of_nodes = 1
    scope.cumulus.create_omega3p_script(omega3p_filename, number_of_nodes=number_of_nodes)

    # Create job and upload files
    create_job(scope, sim_item)
    scope.cumulus.upload_inputs([scope.output_path, scope.model_path])

    # Submit job
    submit_job(scope, sim_item)
    #print 'Submitted job', scope.cumulus.job_id()
  except Exception as ex:
    print 'Exception', ex
    traceback.print_exc()
    ok = False
  finally:
    #release_resources(scope)
    if scope.nersc:
      scope.nersc.logout()

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
  username = get_string(sim_item, 'NERSCAccountName')
  #print 'username', username
  if not username:
    raise Exception('ERROR: NERSC account name not specified')

  password = get_string(sim_item, 'NERSCAccountPassword')
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
def create_job(scope, sim_item):
  '''
  '''
  job_name = get_string(sim_item, 'JobName')
  tail = get_string(sim_item, 'TailFile')
  scope.cumulus.create_job(job_name, tail=tail)

# ---------------------------------------------------------------------
def submit_job(scope, sim_item):
  '''Run the job

  Call this after create_job()
  '''
  # Get inputs
  machine = get_string(sim_item, 'Machine')
  number_of_nodes = get_integer(sim_item, 'NumberOfNodes')
  project_repo = get_string(sim_item, 'NERSCRepository')
  queue = get_string(sim_item, 'Queue')
  timeout_minutes = get_integer(sim_item, 'Timeout')
  scope.cumulus.submit_job(machine, project_repo, timeout_minutes, \
    queue=queue, number_of_nodes=number_of_nodes)

# ---------------------------------------------------------------------
def check_file(path, error_message_format=None):
  '''Confirms that file exists at given path

  Throws an exception if file not found
  '''
  if not error_message_format:
    error_message_format = 'Cannot find file at %s'
  if not os.path.isfile(path):
    raise Exception(error_message_format % scope.model_path)

# ---------------------------------------------------------------------
def get_integer(group_item, name):
  '''Looks for IntItem contained by group.

  Returns either integer value or None if not found
  '''
  item = group_item.find(name)
  if not item:
    print 'WARNING: item \"%s\" not found' % name
    return None

  concrete_item = smtk.attribute.to_concrete(item)
  if concrete_item.type() != smtk.attribute.Item.INT:
    print 'WARNING: item \"%s\" not an integer item' % name
    return None

  return concrete_item.value(0)

# ---------------------------------------------------------------------
def get_string(group_item, name):
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

# ---------------------------------------------------------------------
def setup_results_directory(scope, sim_item):
  '''DEPRECATED Creates and/or clears results directory
  '''
  item = sim_item.find('ResultsDirectory')
  group_item = smtk.attribute.to_concrete(item)

  item = group_item.find('ResultsDirectoryPath')
  dir_item = smtk.attribute.to_concrete(item)
  dir_value = dir_item.value(0)
  if not dir_value:
    raise Exception("Results directory not specified")

  # Check if we should erase the directory first
  item = group_item.find('ClearResultsDirectory')
  if item.isEnabled() and os.path.isdir(dir_value):
    shutil.rmtree(dir_value)

  # Create directory if needed
  if not os.path.isdir(dir_value):
    os.makedirs(dir_value)

  scope.results_directory = dir_value
