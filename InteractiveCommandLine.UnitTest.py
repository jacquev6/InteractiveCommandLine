import unittest

import MockMockMock

from InteractiveCommandLine import *

class TestCase( unittest.TestCase ):
    def setUp( self ):
        self.input = MockMockMock.Mock( "input" )
        self.output = MockMockMock.Mock( "output", self.input )

        self.programOptionHandler = MockMockMock.Mock( "programOptionHandler", self.input )
        self.commandOptionHandler = MockMockMock.Mock( "commandOptionHandler", self.input )
        self.commandHandler = MockMockMock.Mock( "commandHandler", self.input )

        self.commandOption = Option()
        self.commandOption.handle = self.commandOptionHandler.object

        self.programOption = Option()
        self.programOption.handle = self.programOptionHandler.object

        self.command = Command()
        self.command.addOption( "command-option", self.commandOption )
        self.command.handle = self.commandHandler.object

        self.program = Program( self.input.object, self.output.object )
        self.program.addCommand( "test", self.command )
        self.program.addOption( "program-option", self.programOption )

    def tearDown( self ):
        self.input.tearDown()

class CommandLineCommandExecution( TestCase ):
    def testCommandWithoutArguments( self ):
        self.commandHandler.expect()
        self.program._execute( "test" )

    def testCommandWithArguments( self ):
        self.commandHandler.expect( "foo", "bar" )
        self.program._execute( "test", "foo", "bar" )

    def testCommandWithOptionWithoutArguments( self ):
        self.commandOptionHandler.expect().andReturn( [] )
        self.commandHandler.expect()
        self.program._execute( "test", "--command-option" )

    def testCommandWithOptionWithArguments( self ):
        self.commandOptionHandler.expect( "foo", "bar" ).andReturn( [] )
        self.commandHandler.expect()
        self.program._execute( "test", "--command-option", "foo", "bar" )

    def testCommandWithArgumentsWithOptionWithArguments( self ):
        self.commandOptionHandler.expect( "foo", "bar", "baz" ).andReturn( [ "bar", "baz" ] )
        self.commandHandler.expect( "bar", "baz" )
        self.program._execute( "test", "--command-option", "foo", "bar", "baz" )

    def testWithOption( self ):
        self.programOptionHandler.expect( "foo", "test", "--command-option", "bar", "baz" ).andReturn( [ "test", "--command-option", "bar", "baz" ] )
        self.commandOptionHandler.expect( "bar", "baz" ).andReturn( [ "baz" ] )
        self.commandHandler.expect( "baz" )
        self.program._execute( "--program-option", "foo", "test", "--command-option", "bar", "baz" )

class InteractiveCommandExecution( TestCase ):
    def expectInvite( self ):
        self.output.expect.write( ">" )
        return self.input.expect.readline()

    def expectInviteAndReturn( self, line ):
        self.expectInvite().andReturn( line + "\n" )

    def expectInviteAndExit( self ):
        self.expectInvite().andReturn( "" )

    def testCommandWithArguments( self ):
        self.expectInviteAndReturn( "test foo bar" )
        self.commandHandler.expect( "foo", "bar" )
        self.expectInviteAndExit()
        self.program._execute()

unittest.main()
