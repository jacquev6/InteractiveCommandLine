# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of InteractiveCommandLine. http://jacquev6.github.com/InteractiveCommandLine

# InteractiveCommandLine is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# InteractiveCommandLine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with InteractiveCommandLine.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import MockMockMock

from InteractiveCommandLine import Program, Command, Option


class CustomInvite(unittest.TestCase):
    def test(self):
        mocks = MockMockMock.Engine()
        input = mocks.create("input")
        output = mocks.create("output")
        p = Program("program", input.object, output.object, "Custom#")

        output.expect.write("Custom#")
        input.expect.readline().andReturn("")

        p._execute()
