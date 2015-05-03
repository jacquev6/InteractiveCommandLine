# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

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
