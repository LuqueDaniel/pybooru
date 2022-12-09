# -*- coding: utf-8 -*-

"""
Pybooru

Pybooru is a API client written in Python for Danbooru and Moebooru based sites.

Pybooru requires "requests" package to work.

Pybooru modules:
    pybooru -- Main module of Pybooru, contains Pybooru class.
    moebooru -- Contains Moebooru main class.
    danbooru -- Contains Danbooru main class.
    gelbooru -- Contains Gelbooru main class.
    api_moebooru -- Contains all Moebooru API functions.
    api_danbooru -- Contains all Danbooru API functions.
    api_gelbooru -- Contains all Gelbooru API functions.
    exceptions -- Manages and builds Pybooru errors messages.
    resources -- Contains all resources for Pybooru.
"""

__version__ = "5.0.0.dev1"
__license__ = "MIT"
__source_url__ = "https://github.com/LuqueDaniel/pybooru"
__author__ = "Daniel Luque <danielluque14[at]gmail[dot]com>"

# pybooru imports
from .moebooru import Moebooru
from .danbooru import Danbooru
from .gelbooru import Gelbooru
from .e621 import E621
from .exceptions import (PybooruError, PybooruAPIError, PybooruHTTPError)
