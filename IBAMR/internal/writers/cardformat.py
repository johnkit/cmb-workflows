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

from conditionset import ConditionSet

# Default width of first column
DefaultTab = 25

# ---------------------------------------------------------------------
class CardFormat:
  '''Formatter for each output line

  '''

# ---------------------------------------------------------------------
  def __init__(self, keyword,
    att_type=None,
    comment=None,
    if_condition=None,
    item_path=None,
    set_condition=None):
    '''Formatting object for output line

    Required argument:
    keyword: (string) text to write as the IBAMR keyword. If None,
      no output will be written (can be used for comments & conditions)

    Optional arguments:
    att_type: (string) attribute type for this card's info.
      This is typically provided by the writer.
    comment: (string) write comment line
    if_condition: (object) only write output if the condition is in the current
      ConditionSet. The if_condition argument can be an iterable,
      in which case, ALL elements must be in the class' ConditionSet.
    item_path: (string) smtk "path" to item where info can be found
    set_condition: (object) add condition to ConditionSet.
      Is NOT executed if the if_condition fails
    '''
    self.keyword = keyword

    self.att_type = att_type
    self.comment = comment
    if isinstance(if_condition, set):
      self.if_condition = if_condition
    elif hasattr(if_condition, '__iter__'):
      self.if_condition = set(if_condition)
    elif if_condition is not None:
      self.if_condition = set([if_condition])
    else:
      self.if_condition = None
    self.item_path = item_path
    self.set_condition = set_condition

# ---------------------------------------------------------------------
  def write(self, out, att, base_item_path=None, tab=None):
    '''Writes line for input attribute

    Returns boolean indicating if line was written
    '''
    # Skip cards with conditions that don't match
    if not ConditionSet.test_condition(self.if_condition):
      return False

    # Check for comment line
    if self.comment:
      out.write('\n')
      out.write('  // %s\n' % self.comment)
      if not self.keyword:
        return self.finish_write()

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
      self.write_value(
        out, self.keyword, item.isEnabled(), as_boolean=True, tab=tab)
      return self.finish_write()

    if not item.isEnabled():
      return False

    concrete_item = smtk.attribute.to_concrete(item)

    # Skip non-value items
    if not hasattr(concrete_item, 'isSet'):
      return self.finish_write()

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
      self.write_value(
        out, self.keyword, string_value, tab=tab)
      return self.finish_write()

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

    self.write_value(out, keyword, value, tab=tab)
    return self.finish_write()

# ---------------------------------------------------------------------
  def write_value(self, out, keyword, value, as_boolean=False, tab=None):
    '''Writes value to output stream

    '''
    if tab is None:
      tab = DefaultTab
    if len(keyword) > tab:
      tab = len(keyword)
    # Use str.format() method to set first column width
    text_formatter = '  {:<%s} = {:}\n' % tab
    if as_boolean:
      value = 'TRUE' if value else 'FALSE'
    # elif quote_string and isinstance(value, str):
    #   value = '\"%s\"' % value
    line = text_formatter.format(keyword, value)
    out.write(line)

# ---------------------------------------------------------------------
  def finish_write(self):
    '''Internal method for common code after value written. Returns True

    Currently that is checking the set_condition
    '''
    if self.set_condition is not None:
      ConditionSet.set_condition(self.set_condition)
    return True
