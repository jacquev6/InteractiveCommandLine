class Command:
    def __init__( self ):
        pass

class Program:
    def __init__( self ):
        self.__commands = dict()

    def execute( self, arguments ):
        command = arguments[ 1 ]
        self.__commands[ command ].execute()

    def addCommand( self, name, command ):
        self.__commands[ name ] = command
