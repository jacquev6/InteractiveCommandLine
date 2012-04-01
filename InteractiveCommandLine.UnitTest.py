import unittest

import MockMockMock

from InteractiveCommandLine import *

class CommandLineCommandExecution( unittest.TestCase ):
    def setUp( self ):
        self.command = Command()
        self.execute = MockMockMock.Mock( "execute" )
        self.command.execute = self.execute.object
        self.program = Program()
        self.program.addCommand( "test", self.command )

    def tearDown( self ):
        self.execute.tearDown()
    
    def testWithoutArguments( self ):
        self.execute.expect()
        self.program.executeWithArguments( "test" )

    def testWithArguments( self ):
        self.execute.expect( "foo", "bar" )
        self.program.executeWithArguments( "test", "foo", "bar" )

unittest.main()
