import imp
import os
import sys

import smtk

# Hard-code inputs for now
INPUT_SIMULATION_ATTS = 'test1.crf'


# Import GSSHA.py explicitly
module_name = 'GSSHA'
abs_path = os.path.abspath(__file__)
abs_dir = os.path.dirname(abs_path)
module_dir = os.path.join(abs_dir, os.pardir)
#print 'module_dir', module_dir
module_args = imp.find_module(module_name, [module_dir])
imp.load_module(module_name, *module_args)
gssha = sys.modules.get(module_name)
#print 'dir(gssha)', dir(gssha)

#----------------------------------------------------------------------
def load_smtk_model(model_manager, session_type, smtk_file):
  '''Imports and returns smtk model.

  Application should check validity
  '''
  print 'importing model file'
  mgr = smtk.model.Manager.create()
  sess = model_manager.createSession(session_type)
  sess.assignDefaultName()

  op = sess.op("import smtk model")
  #print 'op', op
  op.findFile("filename", smtk.attribute.ALL_CHILDREN).setValue(0, smtk_file)
  #print 'able to operate?', op.ableToOperate()
  result = op.operate()

  outcome = result.findInt('outcome').value(0)
  print 'outcome ok?', outcome == smtk.model.OPERATION_SUCCEEDED
  model = result.findModelEntity('created').value(0)
  print 'model valid?', model.isValid()
  return model

#----------------------------------------------------------------------
def load_attributes(model_manager, att_file):
  '''Reads and returns attribute system
  '''
  print 'loading attribute file'
  att_system = smtk.attribute.System()
  att_system.setRefModelManager(model_manager)
  reader = smtk.io.AttributeReader()
  logger = smtk.io.Logger()
  read_err = reader.read(att_system, att_file, logger)
  print 'read ok?', not read_err
  return att_system

#----------------------------------------------------------------------
def load_resources(model_manager, resource_file):
  '''Reads and returns smtk.common.ResourceSet
  '''
  print 'loading resource file'
  resources = smtk.common.ResourceSet()
  reader = smtk.io.ResourceSetReader()
  logger = smtk.io.Logger()

  hasErrors = reader.readFile(resource_file, resources, logger)
  if hasErrors:
      print "Reader has errors:"
      print logger.convertToString()

  return resources

#----------------------------------------------------------------------
class MockExportSpec:
  '''
  '''
  def __init__(self, sim_atts, export_atts=None):
    self.sim_atts = sim_atts
    self.export_atts = export_atts
    self.logger = smtk.io.Logger()

  def getSimulationAttributes(self):
    return self.sim_atts

  def getExportAttributes(self):
    return self.export_atts

  def getLogger(self):
    return self.logger


#----------------------------------------------------------------------
if __name__ == '__main__':
  model_manager = smtk.model.Manager.create()
  resource_set = load_resources(model_manager, INPUT_SIMULATION_ATTS)

  # Extract attribute systems and construct MockExportSpec
  simbuilder_resource = resource_set.get('simbuilder')
  sim_atts = smtk.attribute.System.CastTo(simbuilder_resource)
  print 'sim_atts', sim_atts

  export_resource = resource_set.get('export')
  export_atts = smtk.attribute.System.CastTo(export_resource)
  print 'export_atts', export_atts

  # Initialize Attribute in export_atts
  export_spec_att = None
  att_list = export_atts.findAttributes('ExportSpec')
  if att_list:
    export_spec_att = att_list[0]
  else:
    export_spec_defn = export_atts.findDefinition('ExportSpec')
    export_spec_att = export_atts.createAttribute(
      'ExportSpec', export_spec_defn)

  name_item = export_spec_att.findString('ProjectName')
  name_item.setValue(0, 'test1')

  path_item = export_spec_att.findDirectory('ProjectPath')
  this_dir = os.path.dirname(os.path.abspath(__file__))
  path_item.setValue(0, this_dir)

  # Create MockExportSpec and run the script
  export_spec = MockExportSpec(sim_atts, export_atts)
  completed = gssha.ExportCMB(export_spec)
  print 'finis, completed:', completed
