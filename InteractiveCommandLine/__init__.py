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


class Option:
    def __init__(self, name, shortHelp):
        self.name = name
        self.shortHelp = shortHelp

    def deactivate(self, *args):
        raise Exception("Option '" + self.name + "' cannot be deactivated")


class _OptionGroup:
    def __init__(self, container, name):
        self.__container = container
        self.__name = name
        self.__groups = list()
        self.__options = list()

    def createOptionGroup(self, name):
        group = _OptionGroup(self.__container, name)
        self.__groups.append(group)
        return group

    def addOption(self, option):
        self.__options.append(option)
        self.__container._addOption(option)

    def _getHelpForOptions(self):
        if len(self.__options) + len(self.__groups) != 0:
            help = recdoc.Section(self.__name)
            if len(self.__options) != 0:
                dl = recdoc.DefinitionList()
                help.add(dl)
                for option in self.__options:
                    dl.add("--" + option.name, option.shortHelp)
            for group in self.__groups:
                help.add(group._getHelpForOptions())
            return help
        else:
            return None


class _OptionContainer(_OptionGroup):
    def __init__(self, name):
        _OptionGroup.__init__(self, self, name)
        self.__options = dict()

    def _addOption(self, option):
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

    def _getUsage(self, options):
        usage = self.name
        if len(self.__options) != 0:
            usage += " [" + options + "]"
        return usage


class Command(_OptionContainer):
    def __init__(self, name, shortHelp):
        _OptionContainer.__init__(self, "Options")
        self.name = name
        self.shortHelp = shortHelp

    def _execute(self, arguments):
        arguments = self._consumeOptions(arguments, "--")
        self.execute(*arguments)


class _CommandGroup:
    def __init__(self, container, name):
        self.__container = container
        self.__name = name
        self.__groups = list()
        self.__commands = list()

    def createCommandGroup(self, name):
        group = _CommandGroup(self.__container, name)
        self.__groups.append(group)
        return group

    def addCommand(self, command):
        self.__commands.append(command)
        self.__container._addCommand(command)

    def _getHelpForCommands(self):
        assert len(self.__commands) + len(self.__groups) != 0
        help = recdoc.Section(self.__name)
        if len(self.__commands) != 0:
            dl = recdoc.DefinitionList()
            help.add(dl)
            for command in self.__commands:
                dl.add(command.name, command.shortHelp)
        for group in self.__groups:
            help.add(group._getHelpForCommands())
        return help


class _CommandContainer(_CommandGroup):
    def __init__(self, name):
        _CommandGroup.__init__(self, self, name)
        self.__commands = dict()

    def _addCommand(self, command):
        self.__commands[command.name] = command

    def _getCommand(self, commandName):
        if commandName in self.__commands:
            return self.__commands[commandName]
        else:
            raise Exception("Unknown command '" + commandName + "'")

    def _executeCommand(self, arguments):
        self._getCommand(arguments[0])._execute(arguments[1:])


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
                self.__output.write(self.__program._getHelp(*args).format())

        self.addCommand(Help(self, self.__output))

    def _getHelp(self, *args):
        doc = recdoc.Document()
        programUsage = self._getUsage("global-options")
        if len(args) == 0:
            commandUsage1 = "command [options]"
            commandUsage2 = programUsage
        else:
            commandName = args[0]
            commandUsage1 = self._getCommand(commandName)._getUsage("options")
            commandUsage2 = commandUsage1

        doc.add(recdoc.Section("Usage").add(recdoc.DefinitionList().add(
            "Command-line mode:", programUsage + " " + commandUsage1
        ).add(
            "Interactive mode:", commandUsage2
        )))
        doc.add(self._getHelpForOptions())

        if len(args) == 0:
            mainSection = self._getHelpForCommands()
        else:
            mainSection = self._getCommand(commandName)._getHelpForOptions()

        doc.add(mainSection)

        return doc

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


class SuperCommand(Command, _CommandContainer):
    def __init__(self, name, shortHelp):
        Command.__init__(self, name, shortHelp)
        _CommandContainer.__init__(self, name)

    def execute(self, *args):
        self._executeCommand(args)
