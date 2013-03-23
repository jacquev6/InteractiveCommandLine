#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of InteractiveCommandLine. http://jacquev6.github.com/InteractiveCommandLine

# InteractiveCommandLine is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# InteractiveCommandLine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with InteractiveCommandLine.  If not, see <http://www.gnu.org/licenses/>.

import setuptools
import textwrap

version = "0.1.0"


if __name__ == "__main__":
    setuptools.setup(
        name="InteractiveCommandLine",
        version=version,
        description="Framework for interactive and command-line programs. Don't use it (yet)",
        author="Vincent Jacques",
        author_email="vincent@vincent-jacques.net",
        url="http://jacquev6.github.com/InteractiveCommandLine",
        long_description=textwrap.dedent("""\
        """),
        packages=[
            "InteractiveCommandLine",
            "InteractiveCommandLine.tests",
        ],
        package_data={
            "InteractiveCommandLine": ["COPYING*"],
        },
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Environment :: Console",
        ],
        test_suite="InteractiveCommandLine.tests.AllTests",
        use_2to3=True
    )
