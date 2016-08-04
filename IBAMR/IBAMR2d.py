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
# Dictionary of formatters for output lines
# Arguments are: (keyword, **kwargs)
# See cardformat.py for full kwargs list
#
# ---------------------------------------------------------------------

# Please order the components alphabetically in this table
card = CardFormat
format_table = {
  'Main': [
    card('solver', att_type='solver', item_path='solver-type'),
    card(None, comment='log file parameters'),
    card('log_file_name', item_path='log/log-file'),
    card('log_all_nodes', item_path='log/log-all-nodes')
  ]
}

# Order the components in the order to be written
comp = OutputComponent
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
