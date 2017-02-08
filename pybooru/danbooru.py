# coding: utf-8 -*-

"""pybooru.danbooru

This module contains Danbooru class for access to API calls, authentication,
build url and return JSON response.

Classes:
   Danbooru -- Danbooru main classs.
"""

# Pybooru imports
from .pybooru import _Pybooru
from .api_danbooru import DanbooruApi_Mixin
from .exceptions import PybooruError


class Danbooru(_Pybooru, DanbooruApi_Mixin):
    """Danbooru class (inherits: Pybooru and DanbooruApi_Mixin).

    To initialize Pybooru, you need to specify one of these two
    parameters: 'site_name' or 'site_url'. If you specify 'site_name', Pybooru
    checks whether there is in the list of default sites (You can get list
    of sites in the 'resources' module).

    To specify a site that isn't in list of default sites, you need use
    'site_url' parameter and specify url.

    Some actions may require you to log in. always specify two parameters to
    log in: 'username' and 'api_key'.

    Attributes:
        site_name (str): Get or set site name set.
        site_url (str): Get or set the URL of Moebooru/Danbooru based site.
        username (str): Return user name.
        api_key (str): Return API key.
        last_call (dict): Return last call.
    """

    def __init__(self, site_name='', site_url='', username='', api_key=''):
        """Initialize Danbooru.

        Keyword arguments:
            site_name (str): Get or set site name set.
            site_url (str): Get or set the URL of Moebooru/Danbooru based site.
            username (str): Your username of the site (Required only for
                            functions that modify the content).
            api_key (str): Your api key of the site (Required only for
                           functions that modify the content).
        """
        super(Danbooru, self).__init__(site_name, site_url, username)

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
            request_args = {'data': params, 'files': file_}

        # Adds auth. Also adds auth if username and api_key are specified
        # Members+ have less restrictions
        if auth is True or self.username and self.api_key is not '':
            if self.username and self.api_key is not '':
                request_args['auth'] = (self.username, self.api_key)
            else:
                raise PybooruError("'username' and 'api_key' attribute of "
                                   "Danbooru are required.")

        # Do call
        return self._request(url, api_call, request_args, method)
