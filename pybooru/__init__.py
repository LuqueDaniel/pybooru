# -*- coding: utf-8 -*-

"""
Pybooru

Pybooru is a API client written in Python for Danbooru and Moebooru based sites.

Pybooru requires "requests" package to work.

Pybooru modules:
    pybooru -- Main module of Pybooru, contains Pybooru class.
    moebooru -- Contains Moebooru main class.
    danbooru -- Contains Danbooru main class.
    api_moebooru -- Contains all Moebooru API functions.
    api_danbooru -- Contains all Danbooru API functions.
    exceptions -- Manages and builds Pybooru errors messages.
    resources -- Contains all resources for Pybooru.
"""

__version__ = "4.1.0"
__license__ = "MIT"
__source_url__ = "http://github.com/LuqueDaniel/pybooru"
__author__ = "Daniel Luque <danielluque14[at]gmail[dot]com>"

# pybooru imports
from .moebooru import Moebooru  # NOQA
from .danbooru import Danbooru  # NOQA
from .exceptions import (PybooruError, PybooruAPIError, PybooruHTTPError)  # NOQA
