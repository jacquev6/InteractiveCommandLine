# -*- coding: utf-8 -*-

# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

import sys
import shlex

class Option:
    def __init__( self ):
        pass

    def consumeArguments( self, arguments ):
        return self.handle( *arguments )

class OptionContainer:
    def __init__( self ):
        self.__options = dict()

    def addOption( self, name, option ):
        self.__options[ name ] = option

    def consumeOptions( self, arguments ):
        goOn = True
        while goOn and len( arguments ) > 0:
            goOn = False
            argument = arguments[ 0 ]
            if argument.startswith( "--" ):
                optionName = argument[ 2: ]
                if optionName in self.__options:
                    arguments = self.__options[ optionName ].consumeArguments( arguments[ 1: ] )
                    goOn = True
        return arguments

class Command( OptionContainer ):
    def execute( self, arguments ):
        arguments = self.consumeOptions( arguments )
        self.handle( *arguments )

class CommandContainer:
    def __init__( self ):
        self.__commands = dict()

    def executeCommand( self, arguments ):
        command = self.__commands[ arguments[ 0 ] ]
        command.execute( arguments[ 1: ] )

    def addCommand( self, name, command ):
        self.__commands[ name ] = command

class Program( CommandContainer, OptionContainer ):
    def __init__( self, input = sys.stdin, output = sys.stdout ):
        CommandContainer.__init__( self )
        OptionContainer.__init__( self )
        self.__input = input
        self.__output = output

    def _execute( self, *arguments ):
        arguments = self.consumeOptions( arguments )
        if len( arguments ) > 0:
            self.executeCommand( arguments )
        else:
            self.startShell()

    def startShell( self ):
        while True:
            self.__output.write( ">" ) # @todo Do not display the ">" when we receive our commands from a pipe
            line = self.__input.readline()
            if line == "":
                break
            arguments = shlex.split( line )
            if len( arguments ) > 0:
                self.executeCommand( arguments )

    def execute( self ): # pragma no cover
        self._execute( *sys.argv[ 1: ] )
