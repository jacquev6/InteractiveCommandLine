import unittest

import MockMockMock

from InteractiveCommandLine import *

class CommandLineCommandExecution( unittest.TestCase ):
    def setUp( self ):
        self.optionHandler = MockMockMock.Mock( "optionHandler" )
        self.commandHandler = MockMockMock.Mock( "commandHandler", self.optionHandler )

        self.option = Option()
        self.option.handle = self.optionHandler.object

        self.command = Command()
        self.command.addOption( "option", self.option )
        self.command.handle = self.commandHandler.object

        self.program = Program()
        self.program.addCommand( "test", self.command )

    def tearDown( self ):
        self.commandHandler.tearDown()
    
    def testWithoutArguments( self ):
        self.commandHandler.expect()
        self.program._execute( "test" )

    def testWithArguments( self ):
        self.commandHandler.expect( "foo", "bar" )
        self.program._execute( "test", "foo", "bar" )

    def testWithOption( self ):
        self.optionHandler.expect( [] ).andReturn( [] )
        self.commandHandler.expect()
        self.program._execute( "test", "--option" )

    def testWithOptionWithArgument( self ):
        self.optionHandler.expect( [ "value" ] ).andReturn( [] )
        self.commandHandler.expect()
        self.program._execute( "test", "--option", "value" )

unittest.main()
