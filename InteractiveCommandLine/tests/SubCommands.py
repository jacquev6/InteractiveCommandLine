# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

import MockMockMock

from InteractiveCommandLine import Program, Command, SuperCommand, Option


class SuperCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.mocks = MockMockMock.Engine()
        self.input = self.mocks.create("input")
        self.output = self.mocks.create("output")

        self.superCommand = SuperCommand("foo", "a super command")

        self.subCommand = Command("bar", "barbaz a frobnicator")
        self.subCommandExecute = self.mocks.create("subCommandExecute")
        self.subCommand.execute = self.subCommandExecute.object
        self.superCommand.addCommand(self.subCommand)

        self.subCommandOption = Option("sub-command-option", "A sub-command option")
        self.subCommandOptionActivate = self.mocks.create("subCommandOptionActivate")
        self.subCommandOption.activate = self.subCommandOptionActivate.object
        self.subCommand.addOption(self.subCommandOption)

        self.superCommandOption = Option("super-command-option", "A super-command option")
        self.superCommandOptionActivate = self.mocks.create("superCommandOptionActivate")
        self.superCommandOption.activate = self.superCommandOptionActivate.object
        self.superCommand.addOption(self.superCommandOption)

        self.program = Program("program", self.input.object, self.output.object)
        self.program.addCommand(self.superCommand)

    def tearDown(self):
        self.mocks.tearDown()

    def testExecute(self):
        self.subCommandExecute.expect()
        self.program._execute("foo", "bar")

    def testExecuteWithSuperCommandOption(self):
        self.superCommandOptionActivate.expect("bar").and_return(["bar"])
        self.subCommandExecute.expect()
        self.program._execute("foo", "--super-command-option", "bar")

    def testExecuteWithSubCommandOption(self):
        self.subCommandOptionActivate.expect().and_return([])
        self.subCommandExecute.expect()
        self.program._execute("foo", "bar", "--sub-command-option")

    def testDoc(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program command [options]
          Interactive mode:   program

        Commands:
          help  Display this help message
          foo   a super command
        """))
        self.program._execute("help")

    def testDocOfSuperCommand(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program foo [foo-options] sub-command [options]
          Interactive mode:   foo [foo-options] sub-command [options]

        Options of command 'foo':
          --super-command-option  A super-command option

        Sub-commands:
          bar  barbaz a frobnicator
        """))
        self.program._execute("help", "foo")

    def testDocOfSubCommand(self):
        self.output.expect.write(textwrap.dedent("""\
        Usage:
          Command-line mode:  program foo [foo-options] bar [bar-options]
          Interactive mode:   foo [foo-options] bar [bar-options]

        Options of command 'foo':
          --super-command-option  A super-command option

        Options of command 'bar':
          --sub-command-option  A sub-command option
        """))
        self.program._execute("help", "foo", "bar")
