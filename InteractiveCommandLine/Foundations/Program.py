# -*- coding: utf-8 -*-

# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of InteractiveCommandLine. http://jacquev6.github.com/InteractiveCommandLine

# InteractiveCommandLine is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# InteractiveCommandLine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with InteractiveCommandLine.  If not, see <http://www.gnu.org/licenses/>.

# Standard library
import sys
import shlex

# Third party libraries
import recdoc

# Project
from .Options import _OptionContainer
from .Commands import Command, _CommandContainer


class Program(_CommandContainer, _OptionContainer):
    def __init__(self, name, input=sys.stdin, output=sys.stdout, invite=">"):
        _CommandContainer.__init__(self, "Commands")
        _OptionContainer.__init__(self, "Global options")
        self.name = name
        self.__input = input
        self.__output = output
        self.__invite = invite
        self.__addAutoHelp()

    def _execute(self, *arguments):
        arguments = self._consumeOptions(arguments, "--")
        if len(arguments) > 0:
            self._executeCommand(arguments)
        else:
            self._startShell()

    def _startShell(self):
        while True:
            try:
                self.__output.write(self.__invite)  # @todo Do not display the ">" when we receive our commands from a pipe
                line = self.__input.readline()
                if line == "":
                    break
                arguments = shlex.split(line)
                arguments = self._consumeOptions(arguments, "+", "-")
                if len(arguments) > 0:
                    self._executeCommand(arguments)
            except Exception as e:
                self.__output.write("ERROR: " + str(e))

    def __addAutoHelp(self):
        class Help(Command):
            def __init__(self, program, output):
                Command.__init__(self, "help", "Display this help message")
                self.__program = program
                self.__output = output

            def execute(self, *args):
                self.__output.write(self.__program._getHelp(args).format())

        self.addCommand(Help(self, self.__output))

    def _getHelp(self, args):
        doc = recdoc.Document()

        doc.add(recdoc.Section("Usage").add(recdoc.DefinitionList().add(
            "Command-line mode:", recdoc.Paragraph(self._getCommandLineUsage(args))
        ).add(
            "Interactive mode:", recdoc.Paragraph(self._getInteractiveUsage(args))
        )))

        for s in self._getHelpSections(args):
            doc.add(s)

        return doc

    def _getCommandLineUsage(self, args):
        programUsage = self._getUsageForOptions("global-options")
        if len(args) == 0:
            return programUsage + " command [options]"
        else:
            commandUsage = self._getCommand(args[0])._getUsage(args[1:])
            return programUsage + " " + commandUsage

    def _getInteractiveUsage(self, args):
        if len(args) == 0:
            return self._getUsageForOptions("global-options")
        else:
            return self._getCommand(args[0])._getUsage(args[1:])

    ### @todo de-duplicate code (with SuperCommand)
    def _getHelpSections(self, args):
        if len(args) == 0:
            return [self._getHelpForOptions(), self._getHelpForCommands()]
        else:
            return [self._getHelpForOptions()] + self._getCommand(args[0])._getHelpSections(args[1:])

    def execute(self):  # pragma no cover
        self._execute(*sys.argv[1:])
