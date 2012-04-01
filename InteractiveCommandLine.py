import sys

class Command:
    def __init__( self ):
        pass

    def addOption( self, name, handler ):
        pass

class Program:
    def __init__( self ):
        self.__commands = dict()

    def execute( self ):
        self.executeWithArguments( *sys.argv[ 1: ] )

    def executeWithArguments( self, *arguments ):
        command = self.__commands[ arguments[ 0 ] ]
        command.execute( *arguments[ 1: ] )

    def addCommand( self, name, command ):
        self.__commands[ name ] = command
