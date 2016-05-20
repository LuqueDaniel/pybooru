# -*- coding: utf-8 -*-

"""
Pybooru
-------

Pybooru is a Python library to access API of Danbooru/Moebooru based sites.
Under MIT license.

Pybooru requires "requests" package to work.

Pybooru modules:
    pybooru -- Main module of Pybooru, contains Pybooru class.
    api -- Contains all Moebooru/Danbooru API functions.
    exceptions -- Manages and builds Pybooru errors messages.
"""

__author__ = "Daniel Luque <danielluque14@gmail.com>"
__version__ = "3.0.1"
__url__ = "http://github.com/LuqueDaniel/pybooru"

# pybooru imports
from .pybooru import Pybooru
from .exceptions import PybooruError
