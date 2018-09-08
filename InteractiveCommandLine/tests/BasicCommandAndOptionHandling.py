# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock

from InteractiveCommandLine import Program, Command, Option


class TestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")

        self.commandOption = Option("command-option", "A command option")
        self.commandOptionActivate = self.mocks.create("commandOptionActivate")
        self.commandOption.activate = self.commandOptionActivate.object

        self.programOption = Option("program-option", "A program option")
        self.programOptionActivate = self.mocks.create("programOptionActivate")
        self.programOption.activate = self.programOptionActivate.object
        self.programOptionDeactivate = self.mocks.create("programOptionDeactivate")
        self.programOption.deactivate = self.programOptionDeactivate.object

        self.command = Command("test", "A test command")
        self.command.addOption(self.commandOption)
        self.commandExecute = self.mocks.create("commandExecute")
        self.command.execute = self.commandExecute.object

        self.program = Program("program", self.input.object, self.output.object)
        self.program.addCommand(self.command)
        self.program.addOption(self.programOption)

    def tearDown(self):
        self.mocks.tearDown()


class CommandLineCommandExecution(TestCase):
    def testCommandWithoutArguments(self):
        self.commandExecute.expect()
        self.program._execute("test")

    def testCommandWithArguments(self):
        self.commandExecute.expect("foo", "bar")
        self.program._execute("test", "foo", "bar")

    def testCommandWithOptionWithoutArguments(self):
        self.commandOptionActivate.expect().and_return([])
        self.commandExecute.expect()
        self.program._execute("test", "--command-option")

    def testCommandWithOptionWithArguments(self):
        self.commandOptionActivate.expect("foo", "bar").and_return([])
        self.commandExecute.expect()
        self.program._execute("test", "--command-option", "foo", "bar")

    def testCommandWithArgumentsWithOptionWithArguments(self):
        self.commandOptionActivate.expect("foo", "bar", "baz").and_return(["bar", "baz"])
        self.commandExecute.expect("bar", "baz")
        self.program._execute("test", "--command-option", "foo", "bar", "baz")

    def testUnknownCommand(self):
        with self.assertRaises(Exception) as cm:
            self.program._execute("unknown")
        self.assertEqual(cm.exception.args[0], "Unknown command 'unknown'")


class CommandLineProgramOptions(TestCase):
    def testOptionWithoutArguments(self):
        self.programOptionActivate.expect("test").and_return(["test"])
        self.commandExecute.expect()
        self.program._execute("--program-option", "test")

    def testOptionWithArguments(self):
        self.programOptionActivate.expect("foo", "test").and_return(["test"])
        self.commandExecute.expect()
        self.program._execute("--program-option", "foo", "test")

    def testUnknownOption(self):
        with self.assertRaises(Exception) as cm:
            self.program._execute("--unknown-option", "foo", "test")
        self.assertEqual(cm.exception.args[0], "Unknown option 'unknown-option'")


class InteractiveCommandExecution(TestCase):
    def expectInvite(self):
        self.output.expect.write(">")
        return self.input.expect.readline()

    def expectInviteAndReturn(self, line):
        self.expectInvite().and_return(line + "\n")

    def expectInviteAndExit(self):
        self.expectInvite().and_return("")

    def testCommandWithArguments(self):
        self.expectInviteAndReturn("test foo bar")
        self.commandExecute.expect("foo", "bar")
        self.expectInviteAndExit()
        self.program._execute()

    def testCommandWithOption(self):
        self.expectInviteAndReturn("test --command-option")
        self.commandOptionActivate.expect().and_return([])
        self.commandExecute.expect()
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionWithoutArgument(self):
        self.expectInviteAndReturn("+program-option")
        self.programOptionActivate.expect().and_return([])
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionWithArguments(self):
        self.expectInviteAndReturn("+program-option foo bar")
        self.programOptionActivate.expect("foo", "bar").and_return([])
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionThenCommand(self):
        self.expectInviteAndReturn("+program-option test")
        self.programOptionActivate.expect("test").and_return(["test"])
        self.commandExecute.expect()
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionDeactivation(self):
        self.expectInviteAndReturn("-program-option")
        self.programOptionDeactivate.expect().and_return([])
        self.expectInviteAndExit()
        self.program._execute()

    def testCommandLineProgramOptionThenCommand(self):
        self.programOptionActivate.expect().and_return([])
        self.expectInviteAndReturn("test")
        self.commandExecute.expect()
        self.expectInviteAndExit()
        self.program._execute("--program-option")

    def testUnknownCommand(self):
        self.expectInviteAndReturn("unknown")
        self.output.expect.write("ERROR: Unknown command 'unknown'")
        self.expectInviteAndExit()
        self.program._execute()

    def testExceptionDuringCommand(self):
        self.expectInviteAndReturn("test")
        self.commandExecute.expect().and_raise(Exception("Command went bad"))
        self.output.expect.write("ERROR: Command went bad")
        self.expectInviteAndExit()
        self.program._execute()

    def testUnknownOption(self):
        self.expectInviteAndReturn("+unknown")
        self.output.expect.write("ERROR: Unknown option 'unknown'")
        self.expectInviteAndExit()
        self.program._execute()

    def testExceptionDuringOptionActivation(self):
        self.expectInviteAndReturn("+program-option")
        self.programOptionActivate.expect().and_raise(Exception("Activation went bad"))
        self.output.expect.write("ERROR: Activation went bad")
        self.expectInviteAndExit()
        self.program._execute()
