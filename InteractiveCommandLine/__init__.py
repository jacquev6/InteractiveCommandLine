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
import recdoc as rd


class Option:
    def __init__(self, name, shortHelp):
        self.name = name
        self.shortHelp = shortHelp

    def deactivate(self, *args):
        raise Exception("Option '" + self.name + "' cannot be deactivated")


class OptionContainer:
    def __init__(self):
        self.__options = dict()

    def addOption(self, option):
        self.__options[option.name] = option

    def _consumeOptions(self, arguments, prefixForActivate, prefixForDeactivate=None):
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

    def _getHelpForOptions(self, title):
        dl = rd.DefinitionList()
        help = rd.Section(title).add(dl)
        for option in sorted(self.__options.itervalues(), key=lambda o: o.name):
            dl.add("--" + option.name, option.shortHelp)
        return help


class Command(OptionContainer):
    def __init__(self, name, shortHelp):
        OptionContainer.__init__(self)
        self.name = name
        self.shortHelp = shortHelp

    def _execute(self, arguments):
        arguments = self._consumeOptions(arguments, "--")
        self.execute(*arguments)


class CommandContainer:
    def __init__(self):
        self.__commands = dict()

    def _executeCommand(self, arguments):
        commandName = arguments[0]
        if commandName in self.__commands:
            command = self.__commands[commandName]
            command._execute(arguments[1:])
        else:
            raise Exception("Unknown command '" + commandName + "'")

    def addCommand(self, command):
        self.__commands[command.name] = command

    def _getHelpForCommands(self):
        dl = rd.DefinitionList()
        help = rd.Section("Commands").add(dl)
        for command in sorted(self.__commands.itervalues(), key=lambda c: c.name):
            dl.add(command.name, command.shortHelp)
        return help

    def _getHelpForCommandOptions(self, commandName):
        return self.__commands[commandName]._getHelpForOptions("Options")

class Program(CommandContainer, OptionContainer):
    def __init__(self, name, input=sys.stdin, output=sys.stdout):
        CommandContainer.__init__(self)
        OptionContainer.__init__(self)
        self.name = name
        self.__input = input
        self.__output = output
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
                self.__output.write(">")  # @todo Do not display the ">" when we receive our commands from a pipe
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
                if len(args) == 0:
                    doc = self.__getHelpForProgram()
                else:
                    doc = self.__getHelpForCommand(args[0])
                self.__output.write(doc.format())

            def __getHelpForProgram(self):
                doc = rd.Document()
                doc.add(rd.Section("Usage").add(rd.Paragraph(
                    "Command-line mode: " + self.__program.name + " [global-options] command [options]\n" +
                    "Interactive mode: " + self.__program.name + " [global-options]"
                )))
                doc.add(self.__program._getHelpForOptions("Global options"))
                doc.add(self.__program._getHelpForCommands())
                return doc

            def __getHelpForCommand(self, commandName):
                doc = rd.Document()
                doc.add(rd.Section("Usage").add(rd.Paragraph(
                    "Command-line mode: " + self.__program.name + " [global-options] " + commandName + " [options]\n" +
                    "Interactive mode: " + commandName + " [options]"
                )))
                doc.add(self.__program._getHelpForOptions("Global options"))
                doc.add(self.__program._getHelpForCommandOptions(commandName))
                return doc

        self.addCommand(Help(self, self.__output))

    def execute(self):  # pragma no cover
        self._execute(*sys.argv[1:])


class StoringOption(Option):
    __noDeactivationValue = (None,)

    def __init__(self, name, shortHelp, container, attribute, activationValue, deactivationValue=__noDeactivationValue):
        Option.__init__(self, name, shortHelp)
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
