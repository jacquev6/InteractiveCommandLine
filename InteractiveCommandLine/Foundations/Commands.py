# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import RecursiveDocument as recdoc

from .Options import _OptionContainer


class Command(_OptionContainer):
    def __init__(self, name, shortHelp):
        _OptionContainer.__init__(self, "Options of command '" + name + "'")
        self.name = name
        self.shortHelp = shortHelp

    def _execute(self, arguments):
        arguments = self._consumeOptions(arguments, "--")
        self.execute(*arguments)

    def _getHelp(self, args):
        return self._getHelpForOptions()

    def _getUsage(self, args):
        return self._getUsageForOptions(self.name + "-options")


class _CommandGroup(object):
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
                dl.add(command.name, recdoc.Paragraph(command.shortHelp))
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
