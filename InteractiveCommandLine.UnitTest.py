import unittest

import MockMockMock

from InteractiveCommandLine import *

class CommandLineProgramTestCase( unittest.TestCase ):
    def testBasicExecution( self ):
        p = Program()
        m = MockMockMock.Mock( "command" )
        m.expect.execute()
        p.addCommand( "test", m.object )
        p.execute( [ "program", "test" ] )
        m.tearDown()

    def testExecutionWithArguments( self ):
        p = Program()
        m = MockMockMock.Mock( "command" )
        m.expect.execute( "foo", "bar" )
        p.addCommand( "test", m.object )
        p.execute( [ "program", "test", "foo", "bar" ] )
        m.tearDown()

unittest.main()
