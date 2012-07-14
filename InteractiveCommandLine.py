import sys

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

    def execute( self, arguments ):
        command = self.__commands[ arguments[ 0 ] ]
        command.execute( arguments[ 1: ] )

    def addCommand( self, name, command ):
        self.__commands[ name ] = command

class Program( CommandContainer, OptionContainer ):
    def __init__( self ):
        CommandContainer.__init__( self )
        OptionContainer.__init__( self )

    def _execute( self, *arguments ):
        arguments = list( arguments )
        arguments = self.consumeOptions( arguments )
        CommandContainer.execute( self, arguments )

    def execute( self ): # pragma no cover
        self._execute( *sys.argv[ 1: ] )
