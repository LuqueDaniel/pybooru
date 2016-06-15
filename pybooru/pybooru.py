# -*- coding: utf-8 -*-

"""pybooru.pybooru

This module contains pybooru main class for access to API calls,
authentication, build urls and return JSON response.

Classes:
   Pybooru -- Main pybooru classs, define Pybooru objectself.
"""

# __furute__ imports
from __future__ import absolute_import
from __future__ import unicode_literals

# pybooru imports
from . import __version__
from .api import ApiFunctionsMixin
from .exceptions import PybooruError
from .resources import SITE_LIST

# External imports
import requests
import hashlib
import re


class Pybooru(ApiFunctionsMixin, object):
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
        site_url: Return the URL of Danbooru/Moebooru based site.
        username: Return user name.
        password: Return password in plain text.
        hash_string: Return hash_string of the site.
    """

    def __init__(self, site_name="", site_url="", username="", password="",
                 hash_string=""):
        """Initialize Pybooru.

        Keyword arguments:
            site_name: The site name in 'SITE_LIST', default sites.
            site_url: URL of on Danbooru/Moebooru based sites.
            hash_string: String that is hashed (required to login).
                         (See the API documentation of the site for more
                         information).
           username: Your username of the site (Required only for functions that
                     modify the content).
           password: Your user password in plain text (Required only for
                     functions that modify the content).
        """
        # Attributes
        self.site_name = site_name.lower()
        self.site_url = site_url.lower()
        self.username = username
        self.password = password
        self.hash_string = hash_string
        self._password_hash = None

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
            self.hash_string = SITE_LIST[self.site_name]['hashed_string']
        else:
            raise PybooruError(
                "The site_name is not valid, specify a valid site_name")

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
                raise PybooruError("Invalid URL", url=self.site_url)
        else:
            raise PybooruError("Invalid URL scheme, use HTTP or HTTPS",
                               url=self.site_url)

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
                self.password_hash = hashlib.sha1(  # pylint: disable=E1101
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
        url = "{0}/{1}.json".format(self.site_url, api_call)

        try:
            if method == 'GET':
                response = self.client.get(url, params=params)
            else:
                if self._password_hash is None:
                    self._build_hash_string()

                params['login'] = self.username
                params['password_hash'] = self.password_hash
                request_args = {'data': params, 'files': file_}

                self.client.headers.update({'content-type': None})
                response = self.client.post(url, **request_args)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise PybooruError("In _request: ", response.status_code,
                               response.url)
        except requests.exceptions.Timeout:
            raise PybooruError("Timeout! in url: {0}".format(response.url))
        except ValueError as err:
            raise PybooruError("JSON Error: {0} in line {1} column {2}".format(
                err.msg, err.lineno, err.colno))
