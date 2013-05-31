# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of InteractiveCommandLine. http://jacquev6.github.com/InteractiveCommandLine

# InteractiveCommandLine is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# InteractiveCommandLine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with InteractiveCommandLine.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import MockMockMock

from InteractiveCommandLine import StoringOption, AppendingOption, ConstantValue, ValueFromOneArgument


class DeactivateableStoringOption(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.attribute = None
        self.activationValue = (42,)
        self.deactivationValue = (56,)
        self.option = StoringOption("name", "short help", self, "attribute", ConstantValue(self.activationValue), ConstantValue(self.deactivationValue))

    def testCOnstructionDoesNotTouchContainer(self):
        self.assertIsNone(self.attribute)

    def testActivateReturnsArguments(self):
        self.assertEqual(self.option.activate("xx", "yy"), ("xx", "yy"))

    def testDeactivateReturnsArguments(self):
        self.assertEqual(self.option.deactivate("xx", "yy"), ("xx", "yy"))

    def testActivateActivates(self):
        self.option.activate()
        self.assertIs(self.attribute, self.activationValue)

    def testDeactivate(self):
        self.option.deactivate()
        self.assertIs(self.attribute, self.deactivationValue)


class NonDeactivateableStoringOption(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.attribute = None
        self.activationValue = (42,)
        self.option = StoringOption("name", "short help", self, "attribute", ConstantValue(self.activationValue))

    def testActivateActivates(self):
        self.option.activate()
        self.assertIs(self.attribute, self.activationValue)

    def testDeactivateRaises(self):
        with self.assertRaises(Exception) as cm:
            self.option.deactivate()
        self.assertEqual(str(cm.exception), "Option 'name' cannot be deactivated")


class StoringOptionFromOneArgument(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.attribute = None
        self.option = StoringOption("name", "short help", self, "attribute", ValueFromOneArgument("FOOS", int))

    def testActivate(self):
        self.assertEqual(self.option.activate("42", "foobar"), ("foobar",))
        self.assertEqual(self.attribute, 42)

    def testHelp(self):
        self.assertEqual(self.option._getHelp()[0], "--name FOOS")


class AppendingOptionTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.attribute = []
        self.option = AppendingOption("name", "add FOO", self.attribute, ValueFromOneArgument("FOO"))

    def testActivateActivates(self):
        self.option.activate("xxx")
        self.assertEqual(self.attribute, ["xxx"])
        self.option.activate("yyy")
        self.assertEqual(self.attribute, ["xxx", "yyy"])
