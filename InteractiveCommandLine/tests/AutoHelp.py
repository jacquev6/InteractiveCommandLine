# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

import MockMockMock

from InteractiveCommandLine import Program, Command, Option, StoringOption, ConstantValue


class AutoHelpWithOptions(unittest.TestCase):
    def setUp(self):
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")

        self.commandOption = Option("command-option", "A command option")

        self.programOption = Option("program-option", "A program option")
        self.storingOption = StoringOption("storing-option", "A storing option", None, None, ConstantValue(True), ConstantValue(False))

        self.command = Command("test", "A test command")
        self.command.addOption(self.commandOption)

        self.program = Program("example", self.input.object, self.output.object)
        self.program.addCommand(self.command)
        self.program.addOption(self.programOption)
        self.program.addOption(self.storingOption)

    def tearDown(self):
        self.mocks.tearDown()

    def testCommandLineProgramHelp(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  example [global-options] command [options]
          Interactive mode:   example [global-options]

        Global options:
          --program-option  A program option
          --storing-option  A storing option

        Commands:
          help  Display this help message
          test  A test command
        """))
        self.program._execute("help")

    def testCommandLineCommandHelp(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  example [global-options] test [test-options]
          Interactive mode:   test [test-options]

        Global options:
          --program-option  A program option
          --storing-option  A storing option

        Options of command 'test':
          --command-option  A command option
        """))
        self.program._execute("help", "test")


class AutoHelpWithoutOptions(unittest.TestCase):
    def setUp(self):
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")

        self.command = Command("test", "A test command")

        self.program = Program("example", self.input.object, self.output.object)
        self.program.addCommand(self.command)

    def tearDown(self):
        self.mocks.tearDown()

    def testCommandLineProgramHelp(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  example command [options]
          Interactive mode:   example

        Commands:
          help  Display this help message
          test  A test command
        """))
        self.program._execute("help")

    def testCommandLineCommandHelp(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  example test
          Interactive mode:   test
        """))
        self.program._execute("help", "test")
