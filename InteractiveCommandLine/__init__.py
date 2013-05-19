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
    def __init__(self, name):
        self.name = name

    def deactivate(self, *args):
        raise Exception("Option '" + self.name + "' cannot be deactivated")


class OptionContainer:
    def __init__(self):
        self.__options = dict()

    def addOption(self, option):
        self.__options[option.name] = option

    def consumeOptions(self, arguments, prefixForActivate, prefixForDeactivate = None):
        goOn = True
        while goOn and len(arguments) > 0:
            goOn = False
            argument = arguments[0]

            optionName = None
            if argument.startswith(prefixForActivate):
                optionName = argument[len(prefixForActivate):]
                mustActivate = True
            elif prefixForDeactivate is not None and argument.startswith(prefixForDeactivate):
                optionName = argument[len(prefixForDeactivate):]
                mustActivate = False

            if optionName is not None:
                if optionName in self.__options:
                    option = self.__options[optionName]
                    operation = option.activate if mustActivate else option.deactivate
                    arguments = operation(*(arguments[1:]))
                    goOn = True
                else:
                    raise Exception("Unknown option '" + optionName + "'")

        return arguments


class Command(OptionContainer):
    def __init__(self, name):
        OptionContainer.__init__(self)
        self.name = name

    def _execute(self, arguments):
        arguments = self.consumeOptions(arguments, "--")
        self.execute(*arguments)


class CommandContainer:
    def __init__(self):
        self.__commands = dict()

    def executeCommand(self, arguments):
        commandName = arguments[0]
        if commandName in self.__commands:
            command = self.__commands[commandName]
            command._execute(arguments[1:])
        else:
            raise Exception("Unknown command '" + commandName + "'")

    def addCommand(self, command):
        self.__commands[command.name] = command


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
            try:
                self.__output.write(">")  # @todo Do not display the ">" when we receive our commands from a pipe
                line = self.__input.readline()
                if line == "":
                    break
                arguments = shlex.split(line)
                arguments = self.consumeOptions(arguments, "+", "-")
                if len(arguments) > 0:
                    self.executeCommand(arguments)
            except Exception as e:
                self.__output.write("ERROR: " + str(e))

    def execute(self):  # pragma no cover
        self._execute(*sys.argv[1:])

class StoringOption(Option):
    __noDeactivationValue = (None,)

    def __init__(self, name, container, attribute, activationValue, deactivationValue = __noDeactivationValue):
        Option.__init__(self, name)
        self.__container = container
        self.__attribute = attribute
        self.__activationValue = activationValue
        self.__deactivationValue = deactivationValue

    def activate(self, *args):
        setattr(self.__container, self.__attribute, self.__activationValue)
        return args

    def deactivate(self, *args):
        if self.__deactivationValue is self.__noDeactivationValue:
            return Option.deactivate(self, *args)
        else:
            setattr(self.__container, self.__attribute, self.__deactivationValue)
            return args
