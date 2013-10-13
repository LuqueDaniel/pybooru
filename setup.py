#!/usr/bin/env python

#setuptools imports
from setuptools import setup
from setuptools import find_packages

#pybooru imports
import pybooru


setup(
    name='Pybooru',
    version=pybooru.__version__,
    author=pybooru.__author__,
    description="Pybooru is a library for Python for access to API Danbooru / Moebooru based sites.",
    author_email="danielluque14 at gmail dot com",
    url="https://github.com/LuqueDaniel/pybooru",
    license="MIT License",
    install_requires=['simplejson'],
    packages=find_packages(),
    include_package_data=True,
)
