#!/usr/bin/env python

# msetuptools imports
from setuptools import setup
from setuptools import find_packages

# pybooru imports
import pybooru


with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='Pybooru',
    version=pybooru.__version__,
    author=pybooru.__author__,
    description="Pybooru is a library for Python for access to API Danbooru / Moebooru based sites.",
    long_description=LONG_DESCRIPTION,
    author_email="danielluque14 at gmail dot com",
    url="https://github.com/LuqueDaniel/pybooru",
    license="MIT License",
    keywords='Pybooru moebooru danbooru API',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
        ],
    platforms=['any'],
    install_requires=['simplejson'],
    packages=find_packages(),
    include_package_data=True,
)
