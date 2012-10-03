#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

__author__ = 'Daniel Luque <danielluque14@gmail.com>'
__version__ = '1.4.9'

setup(
    name='Pybooru',
    version=__version__,
    author=__author__,
    author_email="danielluque14@gmail.com",
    url="https://github.com/LuqueDaniel/pybooru",
    license="MIT License",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['simplejson'],
)
