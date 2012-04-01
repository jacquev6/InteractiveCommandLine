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

unittest.main()
