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
    
    def testCommandWithoutArguments( self ):
        self.commandHandler.expect()
        self.program._execute( "test" )

    def testCommandWithArguments( self ):
        self.commandHandler.expect( "foo", "bar" )
        self.program._execute( "test", "foo", "bar" )

    def testCommandWithOptionWithoutArguments( self ):
        self.optionHandler.expect( [] ).andReturn( [] )
        self.commandHandler.expect()
        self.program._execute( "test", "--option" )

    def testCommandWithOptionWithArguments( self ):
        self.optionHandler.expect( [ "foo", "bar" ] ).andReturn( [] )
        self.commandHandler.expect()
        self.program._execute( "test", "--option", "foo", "bar" )

    def testCommandWithArgumentsWithOptionWithArguments( self ):
        self.optionHandler.expect( [ "foo", "bar", "baz" ] ).andReturn( [ "bar", "baz" ] )
        self.commandHandler.expect( "bar", "baz" )
        self.program._execute( "test", "--option", "foo", "bar", "baz" )

unittest.main()
