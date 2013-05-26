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
import textwrap

import MockMockMock

from InteractiveCommandLine import Program, Command, CommandGroup, Option


class Grouping(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")
        self.p = Program("program", self.input.object, self.output.object)

        self.command = Command("command", "A command in a group")
        self.commandExecute = self.mocks.create("commandExecute")
        self.command.execute = self.commandExecute.object


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.mocks.tearDown()

    def testDoc(self):
        g = self.p.createCommandGroup("Command group")
        g.addCommand(self.command)

        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program [global-options] command [options]
          Interactive mode:   program [global-options]

        Global options:

        Commands:
          help  Display this help message

          Command group:
            command  A command in a group
        """))

        self.p._execute("help")

    def testExecute(self):
        g = self.p.createCommandGroup("Command group")
        g.addCommand(self.command)

        self.commandExecute.expect()

        self.p._execute("command")

    def testExecuteWithRecursiveGroups(self):
        g1 = self.p.createCommandGroup("Command group 1")
        g2 = g1.createCommandGroup("Command group 2")
        g3 = g2.createCommandGroup("Command group 3")
        g3.addCommand(self.command)

        self.commandExecute.expect()

        self.p._execute("command")

    def testDocWithRecursiveGroups(self):
        g1 = self.p.createCommandGroup("Command group 1")
        g2 = g1.createCommandGroup("Command group 2")
        g3 = g2.createCommandGroup("Command group 3")
        g3.addCommand(self.command)

        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program [global-options] command [options]
          Interactive mode:   program [global-options]

        Global options:

        Commands:
          help  Display this help message

          Command group 1:
            Command group 2:
              Command group 3:
                command  A command in a group
        """))

        self.p._execute("help")
