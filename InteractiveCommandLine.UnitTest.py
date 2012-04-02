import unittest

import MockMockMock

from InteractiveCommandLine import *

class CommandLineCommandExecution( unittest.TestCase ):
    def setUp( self ):
        self.command = Command()
        self.optionHandler = MockMockMock.Mock( "optionHandler" )
        self.command.addOption( "option", self.optionHandler )
        self.execute = MockMockMock.Mock( "execute" )
        self.command.execute = self.execute.object
        self.program = Program()
        self.program.addCommand( "test", self.command )

    def tearDown( self ):
        self.execute.tearDown()

    def __executeProgram( self, *arguments ):
        CommandContainer.execute( self.program, *arguments )
    
    def testWithoutArguments( self ):
        self.execute.expect()
        self.__executeProgram( "test" )

    def testWithArguments( self ):
        self.execute.expect( "foo", "bar" )
        self.__executeProgram( "test", "foo", "bar" )

    # def testWithOption( self ):
        # self.optionHandler.expect()
        # self.execute.expect()
        # self.program.executeWithArguments( "test", "--option" )

unittest.main()
