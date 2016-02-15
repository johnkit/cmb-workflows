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
Root export script for GSSHA workflows
"""
import imp
import os
import sys
import smtk

ExportScope = type('ExportScope', (object,), dict())
# ---------------------------------------------------------------------
def ExportCMB(spec):
    '''Entry function, called by CMB to write export files

    Returns boolean indicating success
    Parameters
    ----------
    spec: Top-level object passed in from CMB
    '''
    #print 'Enter ExportCMB()'

    # Initialize scope instance to store spec values and other info
    scope = ExportScope()
    scope.logger = spec.getLogger()
    scope.sim_atts = spec.getSimulationAttributes()
    if scope.sim_atts is not None:
        scope.model_manager = scope.sim_atts.refModelManager()

    scope.export_atts = spec.getExportAttributes()
    if scope.export_atts is not None:
        att_list = scope.export_atts.findAttributes('ExportSpec')
    if not att_list:
        msg = 'No ExportSpec instance -- cannot export'
        print 'WARNING:', msg
        scope.logger.addError(msg)
        return False

    # (else)
    export_spec_att = att_list[0]

    # Get project name
    project_name_item = export_spec_att.findString('ProjectName')
    project_name = project_name_item.value(0)
    if not project_name:
        project_name = 'gssha'
        msg = 'No Project Name specified; using \"%s\"' % project_name
        print 'WARNING:', msg
        scope.logger.addWarning(msg)
    print 'project_name', project_name
    scope.project_name = project_name

    # Initialize project path (folder)
    project_path = None
    item = export_spec_att.find('ProjectPath')
    if item is not None:
        dir_item = smtk.to_concrete(item)
        project_path = dir_item.value(0)
        #print 'project_path', project_path

    if not project_path:
        msg = 'No project_path specified -- cannot export'
        print 'ERROR:', msg
        scope.logger.addWarning(msg)
        return False
    scope.project_path = project_path

    # Create folder if needed
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    completed = write_project_file(scope)
    print 'Export completion status: %s' % completed
    sys.stdout.flush()
    return completed

# ---------------------------------------------------------------------
def write_project_file(scope):
    '''Writes project file
    '''
    tab = 25
    # Use str.format() method to set first column width
    scope.text_formatter = '{:<%s}{:}\n' % tab

    filename = '%s.prj' % scope.project_name
    path = os.path.join(scope.project_path, filename)
    completed = False
    with open(path, 'w') as out:
        out.write('GSSHAPROJECT\n')
        # Todo WMS version
        line = scope.text_formatter.format('PROJECT_PATH', scope.project_path)
        out.write(line)
        completed &= write_grid_specs(scope, out)
        completed &= write_time_specs(scope, out)
        # completed &= write_outlet_point(scope, out)
        # completed &= write_output_frequencies(scope, out)
        # completed &= write_input(scope, out)
        # completed &= write_output(scope, out)
        completed = True

    return completed

# ---------------------------------------------------------------------
def write_grid_specs(scope, out):
    '''Writes grid cards
    '''
    write_header('grid specs', out)
    att = scope.sim_atts.findAttributes('computation')[0]
    group_item = att.findGroup('computation-group')

    item = group_item.find('output-units')
    value = 'METRIC'  # default
    if item.isEnabled():
        value = smtk.attribute.to_concrete.value(0)
    line = '{}\n'.format(value)
    out.write(line)
    return True

# ---------------------------------------------------------------------
def write_time_specs(scope, out):
    '''Writes time specification cards
    '''
    write_header('time specs', out)
    att = scope.sim_atts.findAttributes('computation')[0]
    group_item = att.findGroup('computation-group')

    item = group_item.find('total-time')
    total_time = smtk.attribute.to_concrete(item).value(0)
    line = scope.text_formatter.format('TOT_TIME', total_time)
    out.write(line)

    item = group_item.find('time-step')
    time_step = smtk.attribute.to_concrete(item).value(0)
    line = scope.text_formatter.format('TIMESTEP', time_step)
    out.write(line)

    return True

# ---------------------------------------------------------------------
def write_header(title, out):
    '''
    '''
    comment = '##################'
    comment_line = '%s\n' % comment
    out.write(comment_line)
    title_line = '#{:^16s}#\n'.format(title)
    out.write(title_line)
    out.write(comment_line)
