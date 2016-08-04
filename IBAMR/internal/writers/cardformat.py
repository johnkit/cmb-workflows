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
class CardFormat:
  '''Formatter for each output line

  '''

# ---------------------------------------------------------------------
  def __init__(self, keyword,
    att_type=None,
    item_path=None):
    '''Formatting object for output line

    Required argument:
    keyword: (string) text to write as the IBAMR keyword. If None,
      no output will be written (can be used to set conditions)

    Optional arguments:
    att_type: (string) attribute type for this card's info.
      This is typically provided by the writer.
    item_path: (string) smtk "path" to item where info can be found
    '''
    self.keyword = keyword

    self.att_type = att_type
    self.item_path = item_path

# ---------------------------------------------------------------------
  def write(self, out, att, base_item_path=None):
    '''Writes line for input attribute

    Returns boolean indicating if line was written
    '''
    # Get the item
    full_item_path = self.item_path
    if base_item_path is not None:
      full_item_path = base_item_path
      if self.item_path:
        full_item_path = '/'.join([base_item_path, self.item_path])
    item = att.itemAtPath(full_item_path, '/')
    if item is None:
      print 'ERROR: item not found for attribute %s path %s' % \
        (att.name(), full_item_path)
      return False

    if item.type() == smtk.attribute.Item.VOID:
      self.__class__.write_value(
        out, self.keyword, item.isEnabled(), as_boolean=True)
      return self._finish_write()

    if not item.isEnabled():
      return False

    concrete_item = smtk.attribute.to_concrete(item)

    # If value isn't set, skip
    if not concrete_item.isSet(0):
      return False

    if hasattr(concrete_item, 'numberOfValues') and \
      concrete_item.numberOfValues() > 1:
      value_list = list()
      for i in range(concrete_item.numberOfValues()):
        value_list.append(concrete_item.value(i))
      string_list = [str(x) for x in value_list]
      string_value = ', '.join(string_list)
      self.__class__.write_value(
        out, self.keyword, string_value, quote_string=False)
      return

    # (else) Single value or expression
    keyword = self.keyword
    #property_prefix = 'property_constant'
    value = 'undefined'
    is_expression = False
    if hasattr(concrete_item, 'isExpression') and concrete_item.isExpression(0):
      is_expression = True
      expression_att = concrete_item.expression(0)
      value = expression_att.name()
      if self.expression_keyword is not None:
        keyword = self.expression_keyword
    else:
      value = concrete_item.value(0)
      # RefItem a special case
      if isinstance(value, smtk.AttributePtr):
        value = value.name()

    self.write_value(out, keyword, value)

# ---------------------------------------------------------------------
  def write_value(self, out, keyword, value, as_boolean=False, tab=25):
    '''Writes value to output stream

    '''
    # Use str.format() method to set first column width
    if len(keyword) > tab:
      tab = len(keyword)
    text_formatter = '  {:<%s} = {:}\n' % tab
    if as_boolean:
      value = 'TRUE' if value else 'FALSE'
    # elif quote_string and isinstance(value, str):
    #   value = '\"%s\"' % value
    line = text_formatter.format(keyword, value)
    out.write(line)
