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

from InteractiveCommandLine import Program, Command, Option


class TestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")

        self.commandOption = Option("command-option")
        self.commandOptionActivate = self.mocks.create("commandOptionActivate")
        self.commandOption.activate = self.commandOptionActivate.object

        self.programOption = Option("program-option")
        self.programOptionActivate = self.mocks.create("programOptionActivate")
        self.programOption.activate = self.programOptionActivate.object
        self.programOptionDeactivate = self.mocks.create("programOptionDeactivate")
        self.programOption.deactivate = self.programOptionDeactivate.object

        self.command = Command("test")
        self.command.addOption(self.commandOption)
        self.commandExecute = self.mocks.create("commandExecute")
        self.command.execute = self.commandExecute.object

        self.program = Program(self.input.object, self.output.object)
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
        self.commandOptionActivate.expect().andReturn([])
        self.commandExecute.expect()
        self.program._execute("test", "--command-option")

    def testCommandWithOptionWithArguments(self):
        self.commandOptionActivate.expect("foo", "bar").andReturn([])
        self.commandExecute.expect()
        self.program._execute("test", "--command-option", "foo", "bar")

    def testCommandWithArgumentsWithOptionWithArguments(self):
        self.commandOptionActivate.expect("foo", "bar", "baz").andReturn(["bar", "baz"])
        self.commandExecute.expect("bar", "baz")
        self.program._execute("test", "--command-option", "foo", "bar", "baz")

    def testUnknownCommand(self):
        with self.assertRaises(Exception) as cm:
            self.program._execute("unknown")
        self.assertEqual(cm.exception.args[0], "Unknown command 'unknown'")


class CommandLineProgramOptions(TestCase):
    def testOptionWithoutArguments(self):
        self.programOptionActivate.expect("test").andReturn(["test"])
        self.commandExecute.expect()
        self.program._execute("--program-option", "test")

    def testOptionWithArguments(self):
        self.programOptionActivate.expect("foo", "test").andReturn(["test"])
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
        self.expectInvite().andReturn(line + "\n")

    def expectInviteAndExit(self):
        self.expectInvite().andReturn("")

    def testCommandWithArguments(self):
        self.expectInviteAndReturn("test foo bar")
        self.commandExecute.expect("foo", "bar")
        self.expectInviteAndExit()
        self.program._execute()

    def testCommandWithOption(self):
        self.expectInviteAndReturn("test --command-option")
        self.commandOptionActivate.expect().andReturn([])
        self.commandExecute.expect()
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionWithoutArgument(self):
        self.expectInviteAndReturn("+program-option")
        self.programOptionActivate.expect().andReturn([])
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionWithArguments(self):
        self.expectInviteAndReturn("+program-option foo bar")
        self.programOptionActivate.expect("foo", "bar").andReturn([])
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionThenCommand(self):
        self.expectInviteAndReturn("+program-option test")
        self.programOptionActivate.expect("test").andReturn(["test"])
        self.commandExecute.expect()
        self.expectInviteAndExit()
        self.program._execute()

    def testProgramOptionDeactivation(self):
        self.expectInviteAndReturn("-program-option")
        self.programOptionDeactivate.expect().andReturn([])
        self.expectInviteAndExit()
        self.program._execute()

    def testCommandLineProgramOptionThenCommand(self):
        self.programOptionActivate.expect().andReturn([])
        self.expectInviteAndReturn("test")
        self.commandExecute.expect()
        self.expectInviteAndExit()
        self.program._execute("--program-option")
