# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import RecursiveDocument as recdoc


class Option(object):
    def __init__(self, name, shortHelp):
        self.name = name
        self.shortHelp = shortHelp

    def deactivate(self, *args):
        raise Exception("Option '" + self.name + "' cannot be deactivated")

    def _getHelp(self):
        return ("--" + self.name + "".join(" " + p for p in self._getParameters()), recdoc.Paragraph(self.shortHelp))

    def _getParameters(self):
        return []


class _OptionGroup(object):
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
