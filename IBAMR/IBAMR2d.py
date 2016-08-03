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

"""
import internal
from internal import writer
reload(writer)  # for development

# Predefined strings for "if_condition" arguments
from internal.writer.writer import THERMAL_ANALYSIS, ONLY_THERMAL_ANALYSIS, FLOW_ANALYSIS, \
  VISCOUS_FLOW, INVISCID_FLOW, FLUID_PHASE, MASS_LIMITER, BC_INFLOW, \
  VOID_MATERIAL, ENCLOSURE_RADIATION, MOVING_RADIATION

# ---------------------------------------------------------------------
#
# Dictionary of formatters for output lines
# Arguments are: (keyword, attribute type, item path, **kwargs)
#
# ---------------------------------------------------------------------

# Please order the namelists alphabetically in this table
card = writer.CardFormat
"""

# ---------------------------------------------------------------------
def ExportCMB(spec):
  '''
  Entry function, called by CMB to write export file
  '''
  logger = spec.getLogger()

  # Get export attributes
  export_spec_att = None
  export_atts = spec.getExportAttributes()
  if export_atts is not None:
    att_list = export_atts.findAttributes('ExportSpec')
    if att_list:
      export_spec_att = att_list[0]

  if export_spec_att is None:
    msg = 'No ExportSpec instance -- cannot export'
    print 'WARNING:', msg
    logger.addError(msg)
    return False

  # Get output filename (path)

  # Initialize writer object
  return False
