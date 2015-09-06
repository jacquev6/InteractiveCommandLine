#!/usr/bin/env python
# coding: utf8

# Copyright 2012-2015 Vincent Jacques <vincent@vincent-jacques.net>

import setuptools

version = "0.3.1"


setuptools.setup(
    name="InteractiveCommandLine",
    version=version,
    description="Framework for interactive and command-line programs.",
    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://pythonhosted.org/InteractiveCommandLine",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Environment :: Console",
    ],
    install_requires=["RecursiveDocument"],
    tests_require=["MockMockMock"],
    test_suite="InteractiveCommandLine.tests.AllTests",
    use_2to3=True,
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
        },
    },
)
