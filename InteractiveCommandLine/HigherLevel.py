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

# Project
from .Foundations.Options import Option
from .Foundations.Commands import Command, _CommandContainer


class StoringOption(Option):
    __noDeactivationValue = (None,)

    def __init__(self, name, shortHelp, container, attribute, activationValue, deactivationValue=__noDeactivationValue):
        Option.__init__(self, name, shortHelp)
        self.__container = container
        self.__attribute = attribute
        self.__activationValue = activationValue
        self.__deactivationValue = deactivationValue

    def activate(self, *args):
        value, args = self.__activationValue.extract(args)
        setattr(self.__container, self.__attribute, value)
        return args

    def deactivate(self, *args):
        if self.__deactivationValue is self.__noDeactivationValue:
            return Option.deactivate(self, *args)
        else:
            value, args = self.__deactivationValue.extract(args)
            setattr(self.__container, self.__attribute, value)
            return args

    def _getParameters(self):
        return self.__activationValue.getParameters()


class AppendingOption(Option):
    def __init__(self, name, shortHelp, container, activationValue):
        Option.__init__(self, name, shortHelp)
        self.__container = container
        self.__activationValue = activationValue

    def activate(self, *args):
        value, args = self.__activationValue.extract(args)
        self.__container.append(value)
        return args

    def _getParameters(self):
        return self.__activationValue.getParameters()


class ConstantValue:
    def __init__(self, value):
        self.__value = value

    def extract(self, args):
        return self.__value, args

    def getParameters(self):
        return []


class ValueFromOneArgument:
    def __init__(self, name, parser=lambda s: s):
        self.__name = name
        self.__parser = parser

    def extract(self, args):
        return self.__parser(args[0]), args[1:]

    def getParameters(self):
        return [self.__name]


class SuperCommand(Command, _CommandContainer):
    def __init__(self, name, shortHelp):
        Command.__init__(self, name, shortHelp)
        _CommandContainer.__init__(self, "Sub-commands")

    def execute(self, *args):
        self._executeCommand(args)

    ### @todo de-duplicate code (with Program)
    def _getHelp(self, args):
        help = recdoc.Container().add(self._getHelpForOptions())
        if len(args) == 0:
            return help.add(self._getHelpForCommands())
        else:
            return help.add(self._getCommand(args[0])._getHelp(args[1:]))

    def _getUsage(self, args):
        if len(args) == 0:
            return Command._getUsage(self, args) + " sub-command [options]"
        else:
            return Command._getUsage(self, args) + " " + self._getCommand(args[0])._getUsage(args[1:])
