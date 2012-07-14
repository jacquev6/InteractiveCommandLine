import InteractiveCommandLine as ICL

class ExampleProgram( ICL.Program ):
    def __init__( self ):
        ICL.Program.__init__( self )
        self.addCommand( "echo", self.Echo() )

    class Echo( ICL.Command ):
        def __init__( self ):
            ICL.Command.__init__( self )

        def handle( self, *text ):
            print " ".join( text )

ExampleProgram().execute()
