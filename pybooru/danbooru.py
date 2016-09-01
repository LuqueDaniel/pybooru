# -*- coding: utf-8 -*-

"""pybooru.danbooru

This module contains Danbooru class for access to API calls,
authentication, build url and return JSON response.

Classes:
   Danbooru -- Danbooru classs.
"""

# Pybooru imports
from .pybooru import Pybooru
from .api_danbooru import DanbooruApi


class Danbooru(Pybooru, DanbooruApi):
    """Danbooru class (inherits: Pybooru and DanbooruApi).

    To initialize Pybooru, you need to specify one of these two
    parameters: 'site_name' or 'site_url'. If you specify 'site_name', Pybooru
    checks whether there is in the list of default sites (You can get list
    of sites in the 'resources' module).

    To specify a site that isn't in list of default sites, you need use
    'site_url' parameter and specify url.

    Some actions may require you to log in. always specify two parameters to
    log in: 'username' and 'api_key'. Default sites has an
    associate hash string.

    Attributes:
        site_name: Return site name.
        site_url: Return the URL of Moebooru based site.
        username: Return user name.
        api_key: Return API key.
        last_call: Return last call.
    """

    def __init__(self, site_name="", site_url="", username="", api_key=""):
        super(Danbooru, self).__init__(site_name, site_url, username)
