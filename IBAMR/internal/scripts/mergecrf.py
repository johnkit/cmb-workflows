#!/usr/bin/env python
# Script to load resource file and write to single output,
# i.e., expanding linked files

import os
import sys
import smtk

input_file = 'IBAMR-2d.crf'
this_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(
  this_dir, os.pardir, os.pardir, input_file)
print 'input_path', input_path

crf = None
with open(input_path) as f:
  crf = f.read()
if crf is None:
  print 'Failed to read crf file', input_path
  sys.exit(-1)

resource_set = smtk.common.ResourceSet()
reader = smtk.io.ResourceSetReader()
logger = smtk.io.Logger()

# Read input
has_err = reader.readFile(input_path, resource_set, logger)
if has_err:
  print 'ERROR reading input file', input_path
  print logger.convertToString()
  sys.exit(-1)

# Write into single file
output_file = 'IBAMR-2d-combined.crf'
writer = smtk.io.ResourceSetWriter()
linked_option = smtk.io.ResourceSetWriter.EXPAND_LINKED_FILES
has_err = writer.writeFile(
  output_file, resource_set, logger, linked_option)
if has_err:
  print 'ERROR writing output file', output_file
  print logger.convertToString()
  sys.exit(-2)

sys.exit(0)
