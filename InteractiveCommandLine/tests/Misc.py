# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

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
        input.expect.readline().and_return("")

        p._execute()
