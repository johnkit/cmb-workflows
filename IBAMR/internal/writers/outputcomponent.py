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

import os
print 'loading', os.path.basename(__file__)

import sys
import smtk

# ---------------------------------------------------------------------
class OutputComponent:
  '''Descriptor for components (sections) written to IBAMR file
  '''

# ---------------------------------------------------------------------
  def __init__(self, name, att_type=None, tab=None):
    '''Information for output file component

    Required arguments:
    name: (string) the string written to the IBAMR file

    Optional arguments:
    att_type: (string) type of attribute to use
    tab: (int) tab width for first column (None == use default)
    '''
    self.att_type = att_type
    self.custom_method = None  # not used
    self.name = name
    self.tab = tab
