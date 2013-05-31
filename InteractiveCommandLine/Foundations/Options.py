# -*- coding: utf-8 -*-

# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of InteractiveCommandLine. http://jacquev6.github.com/InteractiveCommandLine

# InteractiveCommandLine is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# InteractiveCommandLine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with InteractiveCommandLine.  If not, see <http://www.gnu.org/licenses/>.

# Third party libraries
import recdoc


class Option:
    def __init__(self, name, shortHelp):
        self.name = name
        self.shortHelp = shortHelp

    def deactivate(self, *args):
        raise Exception("Option '" + self.name + "' cannot be deactivated")

    def _getHelp(self):
        return ("--" + self.name + "".join(" " + p for p in self._getParameters()), recdoc.Paragraph(self.shortHelp))

    def _getParameters(self):
        return []


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
                    dl.add(*option._getHelp())
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

    def _getUsageForOptions(self, options):
        usage = self.name
        if len(self.__options) != 0:
            usage += " [" + options + "]"
        return usage
