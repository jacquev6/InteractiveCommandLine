import unittest

import MockMockMock

from InteractiveCommandLine import *

class CommandLineCommandExecution( unittest.TestCase ):
    def setUp( self ):
        self.command = MockMockMock.Mock( "command" )
        self.program = Program()
        self.program.addCommand( "test", self.command.object )

    def tearDown( self ):
        self.command.tearDown()
    
    def testWithoutArguments( self ):
        self.command.expect.execute()
        self.program.executeWithArguments( "test" )

    def testWithArguments( self ):
        self.command.expect.execute( "foo", "bar" )
        self.program.executeWithArguments( "test", "foo", "bar" )

unittest.main()
