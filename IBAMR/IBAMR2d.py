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
print 'loading', os.path.basename(__file__)
import sys

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
    card('solver', att_type='solver', item_path='solver-type'),
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
  ]
}

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
  comp('Main', att_type='output')
]

# ---------------------------------------------------------------------
def ExportCMB(spec):
  '''
  Entry function, called by CMB to write export file
  '''
  writer = Writer2D(spec)
  return writer.write(component_list, format_table)
