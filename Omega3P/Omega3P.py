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
Export script for Omega3P workflows
"""
import imp
import os
import sys
import smtk

# Explicitly load nersc.py, so that it reloads each time
module_name = 'nersc'
abs_path = os.path.abspath(__file__)
abs_dir = os.path.dirname(abs_path)
module_args = imp.find_module(module_name, [abs_dir])
imp.load_module(module_name, *module_args)
nersc = sys.modules.get(module_name)


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
        model_ents = scope.model_manager.entitiesMatchingFlags(smtk.model.MODEL_ENTITY, True)
        #print 'model_ents', model_ents
        if not model_ents:
            msg = 'No model - cannot export'
            print 'WARNING:', msg
            scope.logger.addWarning(msg)
            print 'Abort export - check logger'
            return False
        elif len(model_ents) > 1:
            msg = 'Multiple models - using first one'
            print 'WARNING:', msg
            scope.logger.addWarning(msg)
        scope.model_ent = model_ents.pop()

    scope.export_atts = spec.getExportAttributes()
    if scope.export_atts is not None:
        att_list = scope.export_atts.findAttributes('ExportSpec')
    if len(att_list) > 1:
        msg = 'More than one ExportSpec instance -- ignoring all'
        print 'WARNING:', msg
        scope.logger.addWarning(msg)
        return False

    # (else)
    export_spec_att = att_list[0]
    scope.model_path = None

    # Initialize output file
    output_path = None
    file_item = export_spec_att.findFile('OutputFile')
    if file_item is not None:
        output_path = file_item.value(0)
        #print 'output_path', output_path

    if not output_path:
        msg = 'No output file specified'
        print 'ERROR:', msg
        scope.logger.addWarning(msg)
        print 'Abort export - check logger'
        return False

    completed = False
    with open(output_path, 'w') as scope.output:
        write_modelinfo(scope)
        write_finiteelement(scope)
        write_pregion(scope)
        write_eigensolver(scope)
        write_port(scope)
        write_postprocess(scope)
        print 'Wrote output file %s' % output_path
        completed = True

    print 'Export completion status: %s' % completed
    sys.stdout.flush()
    if not completed:
        return completed

    # (else)
    # Check for NERSCSimulation item
    sim_item = export_spec_att.find('NERSCSimulation')
    if sim_item is not None and sim_item.isEnabled():
        scope.output_path = output_path
        completed = nersc.submit_omega3p(scope, sim_item)
        print 'Submit to NERSC status: %s' % completed

    return completed

# ---------------------------------------------------------------------
def write_modelinfo(scope):
    '''Writes ModelInfo section to output stream

    '''
    scope.output.write('ModelInfo:\n')
    scope.output.write('{\n')
    urls = scope.model_manager.stringProperty(scope.model_ent, 'url')
    if urls:
        url = urls[0]

        # Get model filename
        scope.model_file = os.path.basename(url)
        print 'scope.model_file', scope.model_file
        scope.output.write('  File: %s\n\n' % scope.model_file)

        # Get full path to model
        if os.path.isabs(url):
            scope.model_path = url
        else:
            smtk_urls = scope.model_manager.stringProperty(
                scope.model_ent, 'smtk_url')
            if smtk_urls:
                smtk_url = smtk_urls[0]
                model_path = os.path.join(smtk_url, url)
                scope.model_path = os.path.abspath(model_path)
        print 'scope.model_path', scope.model_path

    write_boundarycondition(scope)
    write_materials(scope)

    scope.output.write('}\n')

# ---------------------------------------------------------------------
def write_boundarycondition(scope):
    '''Writes SurfaceProperty attributes to output stream

    '''
    atts = scope.sim_atts.findAttributes('SurfaceProperty')
    if not atts:
        return

    name_list = [
        'Electric', 'Magnetic', 'Exterior', 'Impedance', 'Absorbing',
        'Waveguide', 'Periodic']

    scope.output.write('  BoundaryCondition: {\n')

    # Traverse attributes and write BoundaryCondition contents
    surface_material_list = list()  # for saving SurfaceMaterial info
    for att in atts:
        ent_string = format_entity_string(scope, att)
        if not ent_string:
            continue  # warning?

        type_item = att.findString('Type')
        name = type_item.value(0)

        # Periodic BC is special case
        if name == 'Periodic':
            # Write master item
            scope.output.write('    Periodic_M: %s\n' % ent_string)

            # Write slave item
            slave_item = att.findModelEntity('SlaveSurface')
            ent_ref = slave_item.value(0)
            if ent_ref:
                ent = ent_ref.entity()
                prop_idlist = scope.model_manager.integerProperty(ent, 'pedigree id')
                if prop_idlist:
                    scope.output.write('    Periodic_S: %s\n' % prop_idlist[0])
            else:
                print 'WARNING: No slave surface specified for Periodic BC'

            # Write relative phase angle
            phase_item = att.findDouble('Theta')
            phase = phase_item.value(0)
            scope.output.write('    Theta: %f\n' % phase)

            # This completes Periodic case
            continue

        scope.output.write('    %s: %s\n' % (name, ent_string))

        # Check for sigma item
        sigma_item = att.findDouble('Sigma')
        if sigma_item is not None:
            sigma = sigma_item.value(0)
            line1 = '    ReferenceNumber: %s\n' % ent_string
            line2 = '    Sigma: %g\n' % sigma
            text = line1 + line2
            surface_material_list.append(text)
    scope.output.write('  }\n')

    # Traverse surface_material_list and write SurfaceMaterial entries
    for surface_material_string in surface_material_list:
        scope.output.write('\n')
        scope.output.write('  SurfaceMaterial: {\n')
        scope.output.write(surface_material_string)
        scope.output.write('  }\n')

# ---------------------------------------------------------------------
def write_materials(scope):
    '''Writes Material attributes to output stream

    '''
    atts = scope.sim_atts.findAttributes('Material')
    if not atts:
        return

    # Traverse attributes
    for att in atts:
        ent_string = format_entity_string(scope, att)
        if not ent_string:
            continue  # warning?

        scope.output.write('\n')
        scope.output.write('  Material: {\n')
        scope.output.write('    Attribute: %s\n' % ent_string)

        # Make list of (item name, output label) to write
        items_todo = [
            ('Epsilon', 'Epsilon'),
            ('Mu', 'Mu'),
            ('ImgEpsilon', 'EpsilonImag'),
            ('ImgMu', 'MuImag')
        ]
        for item_info in items_todo:
            name, label = item_info
            item = att.findDouble(name)
            if item and item.isEnabled():
                value = item.value(0)
                scope.output.write('    %s: %g\n' % (label, value))

        scope.output.write('  }\n')


# ---------------------------------------------------------------------
def write_finiteelement(scope):
    '''Writes FiniteElement section to output stream

    '''
    scope.output.write('\n')
    scope.output.write('FiniteElement:\n')
    scope.output.write('{\n')

    att = scope.sim_atts.findAttributes('FEInfo')[0]
    order_item = att.findInt('Order')
    scope.output.write('  Order: %d\n' % order_item.value(0))

    curved_surfaces = 'off'
    curved_item = att.find('EnableCurvedSurfaces')
    if curved_item and curved_item.isEnabled():
        curved_surfaces = 'on'
    scope.output.write('  CurvedSurfaces: %s\n' % curved_surfaces)

    scope.output.write('}\n')

# ---------------------------------------------------------------------
def write_pregion(scope):
    '''Writes PRegion section to output stream

    '''
    atts = scope.sim_atts.findAttributes('RegionHighOrder')
    if not atts:
        return

    # Traverse attributes
    for att in atts:
        ent_string = format_entity_string(scope, att)
        if not ent_string:
            continue  # warning?

        order_item = att.findInt('RegionHighOrder')
        order = order_item.value(0)

        scope.output.write('\n')
        scope.output.write('PRegion:\n')
        scope.output.write('{\n')
        scope.output.write('  Type: Material\n')
        scope.output.write('  Reference: %s\n' % ent_string)
        scope.output.write('  Order: %d\n' % order)
        scope.output.write('}\n')

# ---------------------------------------------------------------------
def write_eigensolver(scope):
    '''Writes EigenSolver section to output stream

    '''
    att = scope.sim_atts.findAttributes('EigenSolver')[0]
    scope.output.write('\n')
    scope.output.write('EigenSolver:\n')
    scope.output.write('{\n')

    num_item = att.findInt('NumEigenvalues')
    scope.output.write('  NumEigenvalues: %d\n' % num_item.value(0))
    freq_item = att.findDouble('FrequencyShift')
    scope.output.write('  FrequencyShift: %g\n' % freq_item.value(0))

    scope.output.write('}\n')

# ---------------------------------------------------------------------
def write_port(scope):
    '''Writes Port sections to output stream

    '''
    atts = scope.sim_atts.findAttributes('Port')
    if not atts:
        return

    # Traverse attributes
    for att in atts:
        ent_string = format_entity_string(scope, att)
        if not ent_string:
            continue  # warning?

        mode_item = att.findInt('NumberOfModes')
        num_modes = mode_item.value(0)

        scope.output.write('\n')
        scope.output.write('Port:\n')
        scope.output.write('{\n')
        scope.output.write('  Reference: %s\n' % ent_string)
        scope.output.write('  NumberOfModes: %d\n' % num_modes)
        scope.output.write('}\n')

# ---------------------------------------------------------------------
def write_postprocess(scope):
    '''Writes PostProcess section to output stream

    '''
    att = scope.sim_atts.findAttributes('PostProcess')[0]
    scope.output.write('\n')
    scope.output.write('PostProcess:\n')
    scope.output.write('{\n')
    item = att.find('ModeFiles')
    toggle = 'on' if item.isEnabled() else 'off'
    scope.output.write('  Toggle: %s\n' % toggle)
    scope.output.write('}\n')

# ---------------------------------------------------------------------
def format_entity_string(scope, att):
    '''Generates comma-separated list of "pedigree id"s for model associations

    Returns None if no associations found
    '''
    model_ent_item = att.associations()
    if model_ent_item is None:
        return None

    # Traverse model entities
    ent_idlist = list()
    for i in range(model_ent_item.numberOfValues()):
        ent_ref = model_ent_item.value(i)
        ent = ent_ref.entity()
        prop_idlist = scope.model_manager.integerProperty(ent, 'pedigree id')
        #print 'idlist', idlist
        if prop_idlist:
            #scope.output.write(' %d' % idlist[0])
            ent_idlist.append(prop_idlist[0])

    ent_string = ','.join(str(id) for id in ent_idlist)
    return ent_string
