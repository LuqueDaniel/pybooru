# coding: utf-8 -*-

"""pybooru.e621

This module contains E621 class for access to API calls, authentication,
build url and return JSON response.

Classes:
   E621 -- E621 main classs.
"""

# Pybooru imports
from .pybooru import _Pybooru
from .api_e621 import E621Api_Mixin
from .exceptions import PybooruError

class E621(_Pybooru, E621Api_Mixin):
    """E621 class (inherits: Pybooru and E621Api_Mixin).

    To initialize Pybooru, you need to specify one of these two
    parameters: 'site_name' or 'site_url'. If you specify 'site_name', Pybooru
    checks whether there is in the list of default sites (You can get list
    of sites in the 'resources' module).

    Attributes:
        site_name (str): Get or set site name set.
        site_url (str): Get or set the URL of Moebooru/E621 based site.
        last_call (dict): Return last call.
    """

    def __init__(self, site_name='', site_url='', username='', api_key=''):
        """Initialize E621.

        Keyword arguments:
            site_name (str): Get or set site name set.
            site_url (str): Get or set the URL of Moebooru/E621 based site.
        """
        super(E621, self).__init__(site_name, site_url, username)
        self.api_key = api_key

    def _get(self, api_call, params=None, method='GET', auth=False,
             file_=None):
        """Function to preapre API call.

        Parameters:
            api_call (str): API function to be called.
            params (str): API function parameters.
            method (str): (Defauld: GET) HTTP method (GET, POST, PUT or
                           DELETE)
            file_ (file): File to upload (only uploads).

        Raise:
            PybooruError: When 'username' or 'api_key' are not set.
        """
        url = "{0}/{1}".format(self.site_url, api_call)

        if method == 'GET':
            request_args = {'params': params}
        else:
            raise Exception("Only GET requests are supported")

        # Do call
        return self._request(url, api_call, request_args, method)
