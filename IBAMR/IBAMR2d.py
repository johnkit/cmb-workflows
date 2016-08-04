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
from internal.writers import Writer2D


# ---------------------------------------------------------------------
#
# Dictionary of formatters for output lines
# Arguments are: (keyword, attribute type, item path, **kwargs)
#
# ---------------------------------------------------------------------

# Please order the namelists alphabetically in this table
#card = writer.CardFormat
format_table = {}
component_list = []

# ---------------------------------------------------------------------
def ExportCMB(spec):
  '''
  Entry function, called by CMB to write export file
  '''
  writer = Writer2D(spec)
  return writer.write(component_list, format_table)
