class Command:
    def __init__( self ):
        pass

class Program:
    def __init__( self ):
        self.__commands = dict()

    def execute( self, arguments ):
        pass

    def addCommand( self, name, command ):
        self.__commands[ name ] = command
