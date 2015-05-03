# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

import MockMockMock

from InteractiveCommandLine import Program, Command, Option


class CommandGrouping(unittest.TestCase):
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
          Command-line mode:  program command [options]
          Interactive mode:   program

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
          Command-line mode:  program command [options]
          Interactive mode:   program

        Commands:
          help  Display this help message

          Command group 1:
            Command group 2:
              Command group 3:
                command  A command in a group
        """))

        self.p._execute("help")


class OptionGrouping(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")
        self.p = Program("program", self.input.object, self.output.object)

        self.option = Option("option", "An option in a group")

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.mocks.tearDown()

    def testDoc(self):
        g = self.p.createOptionGroup("Option group")
        g.addOption(self.option)

        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program [global-options] command [options]
          Interactive mode:   program [global-options]

        Global options:
          Option group:
            --option  An option in a group

        Commands:
          help  Display this help message
        """))

        self.p._execute("help")

    def testDocWithRecursiveGroups(self):
        g1 = self.p.createOptionGroup("Option group 1")
        g2 = g1.createOptionGroup("Option group 2")
        g3 = g2.createOptionGroup("Option group 3")
        g3.addOption(self.option)

        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program [global-options] command [options]
          Interactive mode:   program [global-options]

        Global options:
          Option group 1:
            Option group 2:
              Option group 3:
                --option  An option in a group

        Commands:
          help  Display this help message
        """))

        self.p._execute("help")
