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

# Import formatters module explicitly, so that it always reloads
module_name = 'formatters'
abs_path = os.path.abspath(__file__)
abs_dir = os.path.dirname(abs_path)
module_args = imp.find_module(module_name, [abs_dir])
imp.load_module(module_name, *module_args)
formatters = sys.modules.get(module_name)

# ---------------------------------------------------------------------
#
# Dictionary of formatters for project file cards
# Arguments are: (card, attribute type, item path, **kwargs)
#
# ---------------------------------------------------------------------
fmt = formatters.ProjectCardFormat
format_table = {
  'Grid specs': [
    fmt('METRIC', 'computation', 'computation-group/output-units', no_value=True),
    fmt('GRIDSIZE', 'grid', 'grid/gridsize'),
    fmt('ROWS', 'grid', 'grid/rows'),
    fmt('COLS', 'grid', 'grid/columns')
  ],
  'Outlet point info': [],  # Todo
  'Time specs': [
    fmt('TOT_TIME', 'computation', 'computation-group/total-time'),
    fmt('TIMESTEP', 'computation', 'computation-group/time-step')
  ],
  'Output frequencies': [
    fmt('MAP_FREQ', 'computation', 'output-frequencies/map-frequency'),
    fmt('HYD_FREQ', 'computation', 'output-frequencies/hyd-frequency'),
    fmt('MAP_TYPE', 'computation', 'output-frequencies/map-type'),
    fmt('OVERTYPE', 'overland-flow', 'overland-flow/computation-method')
  ],
  'Input': [
    fmt('PRECIP_UNIF', 'precipitation', 'precipitation/rainfall-events',
        if_value='uniform', no_value=True, set_condition='uniform-precip'),
    fmt('RAIN_INTENSITY', 'precipitation', 'precipitation/rainfall-events/intensity',
        if_condition='uniform-precip'),
    fmt('RAIN_DURATION', 'precipitation', 'precipitation/rainfall-events/duration',
        if_condition='uniform-precip'),
    fmt('START_DATE', 'precipitation', 'precipitation/rainfall-events/start',
        if_condition='uniform-precip', is_date=True),
    fmt('START_TIME', 'precipitation', 'precipitation/rainfall-events/start',
        if_condition='uniform-precip', is_time=True)
  ],
  'Output': []  # Todo
}

# List the order to write sections
section_list = [
    'Grid specs',
    'Time specs',
    'Outlet point info',
    'Output frequencies',
    'Input',
    'Output'
]


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

    Basically traverses format_table and calls write() method for each entry.
    '''
    filename = '%s.prj' % scope.project_name
    path = os.path.join(scope.project_path, filename)
    completed = False
    with open(path, 'w') as out:
        out.write('GSSHAPROJECT\n')
        # Todo WMS version
        formatters.write_value(out, 'PROJECT_PATH', scope.project_path)
        # Todo NON_ORTHO_CHANNELS

        for section_title in section_list:
            fmt_list = format_table.get(section_title)
            if fmt_list is None:
                print 'WARNING: section %s not found in format_table' % section_title
            formatters.write_section_title(section_title, out)
            for fmt in fmt_list:
                fmt.write(out, scope.sim_atts)
        completed = True
        print 'Wrote project file', path

    return completed
