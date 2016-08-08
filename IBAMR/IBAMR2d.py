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
Root writer script for IBAMR workflows
"""
import os
import sys
sys.dont_write_bytecode = True
print 'loading', os.path.basename(__file__)

import smtk

import internal
reload(internal)  # for development
from internal.writers import CardFormat, OutputComponent, Writer2D


# ---------------------------------------------------------------------
#
# Dictionary of formatters for individual output lines
# CardFormat init arguments are: (keyword, **kwargs)
# See cardformat.py for full kwargs list
#
# ---------------------------------------------------------------------

card = CardFormat
# Please order the components alphabetically in this table
format_table = {
  'Main': [
    card('solver', att_type='solver', item_path='solver/solver-type'),
    card(None, comment='log file parameters'),
    card('log_file_name', item_path='log/log-file'),
    card('log_all_nodes', item_path='log/log-all-nodes'),

    card(None, item_path='visualization', set_condition='viz-output'),
    card(None, comment='*TODO* visualization parameters', if_condition='viz-output'),
    card('viz_dump_dirname',
      item_path='visualization/directory', if_condition='viz-output'),

    card(None, item_path='restart', set_condition='restart-output'),
    card(None, comment='restart dump parameters', if_condition='restart-output'),
    card('restart_dump_interval',
      item_path='restart/interval', if_condition='restart-output'),
    card('restart_dump_dirname',
      item_path='restart/directory', if_condition='restart-output'),
  ],
  'IBHierarchyIntegrator': [
    card('start_time', item_path='time/start-time'),
    card('end_time', item_path='time/end-time'),
    card('grow_dt', item_path='time/grow-dt'),
    card('num_cycles', item_path='hierarchy-integrator/num-cycles'),
    card('regrid_cfl_interval', item_path='hierarchy-integrator/regrid-cfl-interval'),
    card('dt_max', item_path='time/dt-max'),
    card('error_on_dt_change', item_path='time/error-on-dt-change'),
    card('enable_logging', att_type='output', item_path='enable-logging'),
  ],
  'IBFEMethod':[
    card('IB_delta_fcn', item_path='ib-delta-function'),
    card('split_forces', item_path='split-forces'),
    card('use_jump_conditions', item_path='use-jump-conditions'),
    card('use_consistent_mass_matrix', item_path='use-consistent-mass-matrix'),
    card('IB_point_density', item_path='ib-point-density'),
  ],
}
    #card('', item_path='')

# ---------------------------------------------------------------------
#
# Ordered list of components to write
# OutputComponent init arguments are: (name, **kwargs)
# See outputcomponent.py for full kwargs list
#
# ---------------------------------------------------------------------

comp = OutputComponent
# Order the components in the order to be written
component_list = [
  comp('VelocityBcCoefs_0',
    att_name='velocity0', custom_component_method='write_bc_coefs', tab=16),
  comp('VelocityBcCoefs_1',
    att_name='velocity1', custom_component_method='write_bc_coefs', tab=16),
  comp('VelocityBcCoefs_2',
    att_name='velocity2', custom_component_method='write_bc_coefs', tab=16),
  comp('VelocityBcCoefs_3',
    att_name='velocity3', custom_component_method='write_bc_coefs', tab=16),
  comp('Main', att_type='output'),
  comp('IBHierarchyIntegrator', att_type='solver'),
  comp('IBFEMethod', att_type='solver', base_item_path='fe-method', tab=26),
]

# ---------------------------------------------------------------------
def ExportCMB(spec):
  '''
  Entry function, called by CMB to write export file
  '''
  writer = Writer2D(spec)
  return writer.write(component_list, format_table)
