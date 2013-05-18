# -*- coding: utf-8 -*-

# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of InteractiveCommandLine. http://jacquev6.github.com/InteractiveCommandLine

# InteractiveCommandLine is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# InteractiveCommandLine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with InteractiveCommandLine.  If not, see <http://www.gnu.org/licenses/>.

import sys
import shlex


class Option:
    def __init__(self):
        # Keep this method, even if empty, for derived classes to be able to call it
        pass


class OptionContainer:
    def __init__(self):
        self.__options = dict()

    def addOption(self, name, option):
        self.__options[name] = option

    def consumeOptions(self, arguments, prefixForActivate, prefixForDeactivate = None):
        goOn = True
        while goOn and len(arguments) > 0:
            goOn = False
            argument = arguments[0]
            if argument.startswith(prefixForActivate):
                optionName = argument[len(prefixForActivate):]
                if optionName in self.__options:
                    arguments = self.__options[optionName].activate(*(arguments[1:]))
                    goOn = True
            elif prefixForDeactivate is not None and argument.startswith(prefixForDeactivate):
                optionName = argument[len(prefixForDeactivate):]
                if optionName in self.__options:
                    arguments = self.__options[optionName].deactivate(*(arguments[1:]))
                    goOn = True
        return arguments


class Command(OptionContainer):
    def _execute(self, arguments):
        arguments = self.consumeOptions(arguments, "--")
        self.execute(*arguments)


class CommandContainer:
    def __init__(self):
        self.__commands = dict()

    def executeCommand(self, arguments):
        command = self.__commands[arguments[0]]
        command._execute(arguments[1:])

    def addCommand(self, name, command):
        self.__commands[name] = command


class Program(CommandContainer, OptionContainer):
    def __init__(self, input=sys.stdin, output=sys.stdout):
        CommandContainer.__init__(self)
        OptionContainer.__init__(self)
        self.__input = input
        self.__output = output

    def _execute(self, *arguments):
        arguments = self.consumeOptions(arguments, "--")
        if len(arguments) > 0:
            self.executeCommand(arguments)
        else:
            self.startShell()

    def startShell(self):
        while True:
            self.__output.write(">")  # @todo Do not display the ">" when we receive our commands from a pipe
            line = self.__input.readline()
            if line == "":
                break
            arguments = shlex.split(line)
            arguments = self.consumeOptions(arguments, "+", "-")
            if len(arguments) > 0:
                self.executeCommand(arguments)

    def execute(self):  # pragma no cover
        self._execute(*sys.argv[1:])
