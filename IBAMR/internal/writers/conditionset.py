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

class ConditionSet:
  '''Class for storing objects for condition tests

  Intended to be used as singleton
  '''
  Conditions = set()

  # ---------------------------------------------------------------------
  @classmethod
  def clear(klass):
    klass.Conditions.clear()

  # ---------------------------------------------------------------------
  @classmethod
  def set_condition(klass, condition):
    klass.Conditions.add(condition)

  # ---------------------------------------------------------------------
  @classmethod
  def unset_condition(klass, condition):
    klass.Conditions.discard(condition)  # (no check)

  # ---------------------------------------------------------------------
  @classmethod
  def test_condition(klass, test_condition):
    '''Checks for test_condition in current set

    '''
    # Default case: input has no test _conditions
    if test_condition is None:
      return True

    # Check single string, which is typical case
    if isinstance(test_condition, str):
      return test_condition in klass.Conditions

    # Check if test_conditions are a subset of current conditions
    test_set = None
    if isinstance(test_condition, set):
      test_set = test_condition
    elif hasattr(test_condition, '__iter__'):
      test_set = set(test_condition)
    else:
      test_set = set([test_condition])

    return test_set <= klass.Conditions
