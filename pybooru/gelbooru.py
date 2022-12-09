# coding: utf-8 -*-

"""pybooru.gelbooru

This module contains Gelbooru class for access to API calls, authentication,
build url and return JSON response.

Classes:
   Gelbooru -- Gelbooru main classs.
"""

# Pybooru imports
from .pybooru import _Pybooru
from .api_gelbooru import GelbooruApi_Mixin
from .exceptions import PybooruError


class Gelbooru(_Pybooru, GelbooruApi_Mixin):
    """Gelbooru class (inherits: Pybooru and GelbooruApi_Mixin).

    To initialize Pybooru, you need to specify one of these two
    parameters: 'site_name' or 'site_url'. If you specify 'site_name', Pybooru
    checks whether there is in the list of default sites (You can get list
    of sites in the 'resources' module).

    Attributes:
        site_name (str): Get or set site name set.
        site_url (str): Get or set the URL of Moebooru/Gelbooru based site.
        username (str): Return user name.
        api_key (str): Return API key.
        last_call (dict): Return last call.
    """

    def __init__(self, site_name='', site_url='', username='', api_key=''):
        """Initialize Gelbooru.

        Keyword arguments:
            site_name (str): Get or set site name set.
            site_url (str): Get or set the URL of Moebooru/Gelbooru based site.
            username (str): Your username of the site (Required only for
                            functions that modify the content).
            api_key (str): Your api key of the site (Required only for
                           functions that modify the content).
        """
        super(Gelbooru, self).__init__(site_name, site_url, username)
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
        url = "{0}/index.php?page=dapi&s={1}&q=index&json=1".format(self.site_url, api_call)

        if method == 'GET':
            request_args = {'params': params}
        else:
            raise Exception("Only GET requests are supported")

        # Adds auth. Also adds auth if username and api_key are specified
        # Members+ have less restrictions
        if auth or (self.username and self.api_key):
            if self.username and self.api_key:
                request_args['auth'] = (self.username, self.api_key)
            else:
                raise PybooruError("'username' and 'api_key' attribute of "
                                   "Danbooru are required.")

        # Do call
        return self._request(url, api_call, request_args, method)

    def _get_xml(self, api_call, params=None):
        url = "{0}/index.php?page=dapi&s={1}&q=index".format(self.site_url, api_call)
        request_args = {'params': params}
        return self._request_xml(url, api_call, request_args)
