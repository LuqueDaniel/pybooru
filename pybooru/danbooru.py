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
from .exceptions import PybooruError


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
    associate API key.

    Attributes:
        site_name: Return site name.
        site_url: Return the URL of Moebooru based site.
        username: Return user name.
        api_key: Return API key.
        last_call: Return last call.
    """

    def __init__(self, site_name="", site_url="", username="", api_key=""):
        super(Danbooru, self).__init__(site_name, site_url, username)

        if api_key is not "":
            self.api_key = api_key

    def _get(self, api_call, params=None, method='GET', auth=False,
             file_=None):
        url = "{0}/{1}".format(self.site_url, api_call)

        if method == 'GET':
            request_args = {'params': params}
        else:
            request_args = {'data': params, 'files': file_}

        # Adds auth
        if auth is True:
            try:
                request_args['auth'] = (self.username, self.api_key)
            except AttributeError:
                raise PybooruError("'username' and 'api_key' attribute of \
                                   Danbooru are required.")

        # Do call
        return self._request(url, api_call, request_args, method)
