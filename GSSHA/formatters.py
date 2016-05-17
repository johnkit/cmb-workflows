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
GSSHA formatting classes & functions
"""
import os
import sys
import smtk


# ---------------------------------------------------------------------
def write_section_title(title, out):
  '''Write comment lines with title
  '''
  comment_line = '####################\n'
  out.write(comment_line)
  title_line = '#{:^18s}#\n'.format(title)
  out.write(title_line)
  out.write(comment_line)

# ---------------------------------------------------------------------
def write_value(out, card, value):
  '''Writes value to project file

  '''
  tab = 25
  # Use str.format() method to set first column width
  text_formatter = '{:<%s}{:}\n' % tab
  line = text_formatter.format(card, value)
  out.write(line)

# ---------------------------------------------------------------------
class ProjectCardFormat:
  '''Formatter for GSSHA project cards

  '''
  # Shared/static conditions
  conditions = set()

# ---------------------------------------------------------------------
  def __init__(self, card, att_type, item_path,
               if_condition=None,
               if_value=None,
               is_date=False,
               is_time=False,
               no_value=False,
               set_condition=False):
    '''Formatting object for project file output card

    Required arguments:
    card: (string) card text
    att_type: (string) attribute type where info can be found
    item_path: (string) smtk "path" to item where info can be found

    Optional arguments:
    if_condition: only write output if condition is in the class' conditions var
    if_value: only write output if item's value == if_value
              also only apply set_condition if item's value == if_value.
              Ignored when either is_date or is_time is set
    is_date: item is a group item in our standard form of year/month/day
    is_time: item is a group item with our standard form of hour/min
    no_value: (boolean) flag indicating that no value is written for this card,
                        just the card itself
    set_condition: insert condition in class conditions set;
                   not executed when if_condition or if_value fail
    '''
    self.card = card
    self.att_type = att_type
    self.item_path = item_path
    self.if_condition = if_condition
    self.if_value = if_value
    self.is_date = is_date
    self.is_time = is_time
    self.no_value = no_value
    self.set_condition = set_condition

# ---------------------------------------------------------------------
  def write(self, out, att_or_system):
    '''Write output card

    out: (file) stream to write output to
    att_or_system: Either smtk.attribute.System or smtk.attribute.Attribute.
                   If System passed in, attribute must be single instance.
    '''
    #print 'Writing', self.card
    #print 'att_or_system', att_or_system

    # Check for if_condition
    if self.if_condition:
      has_condition = self.if_condition in self.__class__.conditions
      if not has_condition:
        return True

    att = None

    # Check input type (don't forget shared pointer type!)
    if isinstance(att_or_system, smtk.attribute.Attribute) or \
      isinstance(att_or_system, smtk.AttributePtr):
      att = att_or_system

    # If attribute system passed in, look for 1 attribute instance
    elif isinstance(att_or_system, smtk.attribute.System) or \
      isinstance(att_or_system, smtk.SystemPtr):
      sim_atts = att_or_system
      att_list = sim_atts.findAttributes(self.att_type)
      if not att_list:
        print 'ERROR: Attribute not found, type', self.att_type
        return False

      if len(att_list) > 1:
        print 'ERROR: Multiple attributes found, type', self.att_type
        return False

      # (else)
      att = att_list[0]

    if att is None:
      # Safety first
      print 'Invalid input: att_or_system is not attribute or attribute system'
      return False

    item = att.itemAtPath(self.item_path, '/')
    if item is None:
      print 'ERROR: item not found for attribute %s path %s' % \
        (att.name(), self.item_path)
      return False

    if not item.isEnabled():
      return False

    if self.no_value:
      line = '%s\n' % self.card
      out.write(line)
    elif self.is_date:
      item_names = ['year', 'month', 'day']
      self._write_string_list(out, item, item_names, 2)
    elif self.is_time:
      item_names = ['hour', 'minute']
      self._write_string_list(out, item, item_names, 2)
    else:
      concrete_item = smtk.attribute.to_concrete(item)
      value = concrete_item.value(0)

      # Check if_value
      if self.if_value is not None:
        if value != self.if_value:
          return True

      self.write_value(out, value)

    # Check set_condition
    if self.set_condition is not None:
      self.__class__.conditions.add(self.set_condition)

    return True

# ---------------------------------------------------------------------
  def write_value(self, out, value):
    '''Writes value to output stream

    '''
    # Call static function
    write_value(out, self.card, value)

# ---------------------------------------------------------------------
  def _write_string_list(self, out, parent_item, child_item_names,
    zfill_size=None):
    '''Constructs string from list of item names

    Returns string, or None if error occurs
    '''
    if parent_item.type() != smtk.attribute.Item.GROUP:
      print 'ERROR: item %s is not a group item' % parent_item.name()
      return None
    group_item = smtk.attribute.to_concrete(parent_item)

    string_list = list()
    for child_name in child_item_names:
      item = group_item.find(child_name)
      if item is None:
        print 'ERROR: item %s contains no %s child' % \
          (parent_item.name(), child_name)
        return None

      child_item = smtk.attribute.to_concrete(item)
      # if child_item.type() != smtk.attribute.Item.INT:
      #   print 'ERROR item %s is not type integer' % item_type
      #   return False

      string_value = child_item.valueAsString(0)
      if zfill_size:
        string_value = string_value.zfill(zfill_size)
      string_list.append(string_value)

    if string_list:
      formatted_string = ' '.join(string_list)
      self.write_value(out, formatted_string)

    return True
