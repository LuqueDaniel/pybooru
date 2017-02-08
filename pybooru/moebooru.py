# -*- coding: utf-8 -*-

"""pybooru.moebooru

This module contains Moebooru class for access to API calls,
authentication, build url and return JSON response.

Classes:
   Moebooru -- Moebooru classs.
"""

# __furute__ imports
from __future__ import absolute_import

# External imports
import hashlib

# Pybooru imports
from .pybooru import _Pybooru
from .api_moebooru import MoebooruApi_Mixin
from .exceptions import PybooruError
from .resources import SITE_LIST


class Moebooru(_Pybooru, MoebooruApi_Mixin):
    """Moebooru class (inherits: Pybooru and MoebooruApi_Mixin).

    To initialize Pybooru, you need to specify one of these two
    parameters: 'site_name' or 'site_url'. If you specify 'site_name', Pybooru
    checks whether there is in the list of default sites (You can get list
    of sites in the 'resources' module).

    To specify a site that isn't in list of default sites, you need use
    'site_url' parameter and specify url.

    Some actions may require you to log in. always specify three parameters to
    log in: 'hash_string', 'username' and 'password'. Default sites has an
    associate hash string.

    Attributes:
        site_name (str): Get or set site name set.
        site_url (str): Get or set the URL of Moebooru/Danbooru based site.
        api_version (str): Version of Moebooru API.
        username (str): Return user name.
        password (str): Return password in plain text.
        hash_string (str): Return hash_string of the site.
        last_call (dict) last call.
    """

    def __init__(self, site_name='', site_url='', username='', password='',
                 hash_string='', api_version='1.13.0+update.3'):
        """Initialize Moebooru.

        Keyword arguments:
            site_name (str): Get or set site name set.
            site_url (str): Get or set the URL of Moebooru/Danbooru based site.
            api_version (str): Version of Moebooru API.
            hash_string (str): String that is hashed (required to login).
                               (See the API documentation of the site for more
                               information).
            username (str): Your username of the site (Required only for
                             functions that modify the content).
            password (str): Your user password in plain text (Required only
                            for functions that modify the content).
        """
        super(Moebooru, self).__init__(site_name, site_url, username)

        self.api_version = api_version.lower()
        self.password = password
        self.password_hash = None

    def _build_url(self, api_call):
        """Build request url.

        Parameters:
            api_call (str): Base API Call.

        Returns:
            Complete url (str).
        """
        if self.api_version in ('1.13.0', '1.13.0+update.1', '1.13.0+update.2'):
            if '/' not in api_call:
                return "{0}/{1}/index.json".format(self.site_url, api_call)
        return "{0}/{1}.json".format(self.site_url, api_call)

    def _build_hash_string(self):
        """Function for build password hash string.

        Raises:
            PybooruError: When isn't provide hash string.
            PybooruError: When aren't provide username or password.
            PybooruError: When Pybooru can't add password to hash strring.
        """
        # Build AUTENTICATION hash_string
        # Check if hash_string exists
        if self.site_name in SITE_LIST or self.hash_string is not "":
            if self.username and self.password is not "":
                try:
                    hash_string = self.hash_string.format(self.password)
                except TypeError:
                    raise PybooruError("Pybooru can't add 'password' "
                                       "to 'hash_string'")
                # encrypt hashed_string to SHA1 and return hexdigest string
                self.password_hash = hashlib.sha1(
                    hash_string.encode('utf-8')).hexdigest()
            else:
                raise PybooruError("Specify the 'username' and 'password' "
                                   "parameters of the Pybooru object, for "
                                   "setting 'password_hash' attribute.")
        else:
            raise PybooruError(
                "Specify the 'hash_string' parameter of the Pybooru"
                " object, for the functions that requires login.")

    def _get(self, api_call, params, method='GET', file_=None):
        """Function to preapre API call.

        Parameters:
            api_call (str): API function to be called.
            params (dict): API function parameters.
            method (str): (Defauld: GET) HTTP method 'GET' or 'POST'
            file_ (file): File to upload.
        """
        url = self._build_url(api_call)

        if method == 'GET':
            request_args = {'params': params}
        else:
            if self.password_hash is None:
                self._build_hash_string()

            # Set login
            params['login'] = self.username
            params['password_hash'] = self.password_hash
            request_args = {'data': params, 'files': file_}

        # Do call
        return self._request(url, api_call, request_args, method)
