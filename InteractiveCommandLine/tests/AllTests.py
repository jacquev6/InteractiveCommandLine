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

        self.programOptionHandler = self.mocks.create("programOptionHandler")
        self.commandOptionHandler = self.mocks.create("commandOptionHandler")
        self.commandHandler = self.mocks.create("commandHandler")

        self.commandOption = Option()
        self.commandOption.handle = self.commandOptionHandler.object

        self.programOption = Option()
        self.programOption.handle = self.programOptionHandler.object

        self.command = Command()
        self.command.addOption("command-option", self.commandOption)
        self.command.handle = self.commandHandler.object

        self.program = Program(self.input.object, self.output.object)
        self.program.addCommand("test", self.command)
        self.program.addOption("program-option", self.programOption)

    def tearDown(self):
        self.mocks.tearDown()


class CommandLineCommandExecution(TestCase):
    def testCommandWithoutArguments(self):
        self.commandHandler.expect()
        self.program._execute("test")

    def testCommandWithArguments(self):
        self.commandHandler.expect("foo", "bar")
        self.program._execute("test", "foo", "bar")

    def testCommandWithOptionWithoutArguments(self):
        self.commandOptionHandler.expect().andReturn([])
        self.commandHandler.expect()
        self.program._execute("test", "--command-option")

    def testCommandWithOptionWithArguments(self):
        self.commandOptionHandler.expect("foo", "bar").andReturn([])
        self.commandHandler.expect()
        self.program._execute("test", "--command-option", "foo", "bar")

    def testCommandWithArgumentsWithOptionWithArguments(self):
        self.commandOptionHandler.expect("foo", "bar", "baz").andReturn(["bar", "baz"])
        self.commandHandler.expect("bar", "baz")
        self.program._execute("test", "--command-option", "foo", "bar", "baz")

    def testWithOption(self):
        self.programOptionHandler.expect("foo", "test", "--command-option", "bar", "baz").andReturn(["test", "--command-option", "bar", "baz"])
        self.commandOptionHandler.expect("bar", "baz").andReturn(["baz"])
        self.commandHandler.expect("baz")
        self.program._execute("--program-option", "foo", "test", "--command-option", "bar", "baz")


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
        self.commandHandler.expect("foo", "bar")
        self.expectInviteAndExit()
        self.program._execute()
