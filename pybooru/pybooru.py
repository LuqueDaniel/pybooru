# -*- coding: utf-8 -*-

"""pybooru.pybooru

This module contains pybooru main class for access to API calls,
authentication, build urls and return JSON response.

Classes:
   Pybooru -- Main pybooru classs, define Pybooru objectself.
"""

# __furute__ imports
from __future__ import absolute_import

# pybooru imports
from . import __version__
from .api import ApiFunctionsMixin
from .exceptions import (PybooruError, PybooruHTTPError)
from .resources import (SITE_LIST, HTTP_STATUS_CODE)

# External imports
import requests
import hashlib
import re


class Pybooru(ApiFunctionsMixin):
    """Pybooru main class (inherits: pybooru.api.ApiFunctionsMixin).

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
        site_name: Return site name.
        site_url: Return the URL of Moebooru based site.
        api_version: Version of Moebooru API.
        username: Return user name.
        password: Return password in plain text.
        hash_string: Return hash_string of the site.
        last_call: Return last call.
    """

    def __init__(self, site_name="", site_url="", username="", password="",
                 hash_string="", api_version="1.13.0+update.3"):
        """Initialize Pybooru.

        Keyword arguments:
            site_name: The site name in 'SITE_LIST', default sites.
            site_url: URL of on Moebooru based sites.
            api_version: Version of Moebooru API.
            hash_string: String that is hashed (required to login).
                         (See the API documentation of the site for more
                         information).
            username: Your username of the site (Required only for functions
                     that modify the content).
            password: Your user password in plain text (Required only for
                     functions that modify the content).
        """
        # Attributes
        self.site_name = site_name.lower()
        self.site_url = site_url.lower()
        self.api_version = api_version.lower()
        self.username = username
        self.password = password
        self.hash_string = hash_string
        self.password_hash = None
        self.last_call = {}

        # Set HTTP Client
        self.client = requests.Session()
        headers = {'user-agent': 'Pybooru/{0}'.format(__version__),
                   'content-type': 'application/json; charset=utf-8'}
        self.client.headers = headers

        # Validate site_name or site_url
        if site_url or site_name is not "":
            if site_name is not "":
                self._site_name_validator()
            elif site_url is not "":
                self._url_validator()
        else:
            raise PybooruError("Unexpected empty strings,"
                               " specify parameter 'site_name' or 'site_url'.")

    def _site_name_validator(self):
        """Function that checks the site name and get url."""
        if self.site_name in SITE_LIST:
            self.site_url = SITE_LIST[self.site_name]['url']
            self.api_version = SITE_LIST[self.site_name]['api_version']
            self.hash_string = SITE_LIST[self.site_name]['hashed_string']
        else:
            raise PybooruError(
                "The 'site_name' is not valid, specify a valid 'site_name'.")

    def _url_validator(self):
        """URL validator for site_url attribute."""
        # Regular expression to URL validate
        regex = re.compile(
            r'^(?:http|https)://'  # Scheme only HTTP/HTTPS
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?| \
            [A-Z0-9-]{2,}(?<!-)\.?)|'  # Domain
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # or ipv6
            r'(?::\d+)?'  # Port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # Validate URL
        if re.match('^(?:http|https)://', self.site_url):
            if not re.search(regex, self.site_url):
                raise PybooruError("Invalid URL: {0}".format(self.site_url))
        else:
            raise PybooruError("Invalid URL scheme, use HTTP "
                               "or HTTPS: {0}".format(self.site_url))

    @staticmethod
    def _get_status(status_code):
        """Get status message."""
        if status_code in HTTP_STATUS_CODE:
            return "{0}, {1}".format(*HTTP_STATUS_CODE[status_code])
        else:
            return None

    def _build_url(self, api_call):
        """Build request url.

        Parameters:
            api_call: Base API Call.
        """
        if self.api_version in ('1.13.0', '1.13.0+update.1', '1.13.0+update.2'):
            if '/' not in api_call:
                return "{0}/{1}/index.json".format(self.site_url, api_call)

        return "{0}/{1}.json".format(self.site_url, api_call)

    def _build_hash_string(self):
        """Function for build password hash string."""
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

    def _request(self, api_call, params, method='GET', file_=None):
        """Function to request and returning JSON data.

        Parameters:
            api_call: API function to be called.
            params: API function parameters.
            method: (Defauld: GET) HTTP method 'GET' or 'POST'
            file_: File to upload.
        """
        # Build url
        url = self._build_url(api_call)

        try:
            if method == 'GET':
                response = self.client.request(method, url, params=params)
            else:
                if self.password_hash is None:
                    self._build_hash_string()

                params['login'] = self.username
                params['password_hash'] = self.password_hash
                request_args = {'data': params, 'files': file_}

                self.client.headers.update({'content-type': None})
                response = self.client.request(method, url, **request_args)

            self.last_call.update({
                'API': api_call,
                'url': response.url,
                'status_code': response.status_code,
                'status': self._get_status(response.status_code),
                'headers': response.headers
                })

            if response.status_code is 200:
                return response.json()
            else:
                raise PybooruHTTPError("In _request", response.status_code,
                                       response.url)
        except requests.exceptions.Timeout:
            raise PybooruError("Timeout! in url: {0}".format(response.url))
        except ValueError as e:
            raise PybooruError("JSON Error: {0} in line {1} column {2}".format(
                                e.msg, e.lineno, e.colno))
