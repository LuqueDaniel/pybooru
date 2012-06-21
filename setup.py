#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

__author__ = 'Daniel Luque <danielluque14@gmail.com>'
__version__ = '1.3.1'

setup(
    name='pybooru',
    version=__version__,
    author=__author__,
    author_email="danielluque14@gmail.com",  
    url="https://github.com/LuqueDaniel/pybooru",  
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['simplejson'],
)