import InteractiveCommandLine as ICL

class ExampleProgram( ICL.Program ):
    def __init__( self ):
        ICL.Program.__init__( self )
        self.addCommand( "echo", self.Echo( self ) )
        self.addOption( "verbose", self.Verbose( self ) )
        self.verbose = False

    class Verbose( ICL.Option ):
        def __init__( self, program ):
            ICL.Option.__init__( self )
            self.__program = program

        def handle( self, *args ):
            self.__program.verbose = True
            return args

    class Echo( ICL.Command ):
        def __init__( self, program ):
            ICL.Command.__init__( self )
            self.__program = program
            self.upper = False
            self.addOption( "upper", self.Upper( self ) )

        class Upper( ICL.Option ):
            def __init__( self, echo ):
                ICL.Option.__init__( self )
                self.__echo = echo

            def handle( self, *args ):
                self.__echo.upper = True
                return args

        def handle( self, *text ):
            toPrint = " ".join( text )
            if self.__program.verbose:
                toPrint = "Verbose " + toPrint
            if self.upper:
                toPrint = toPrint.upper()
            print toPrint

ExampleProgram().execute()
