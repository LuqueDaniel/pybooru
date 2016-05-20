# -*- coding: utf-8 -*-

"""This module contains pybooru object class."""

# __furute__ imports
from __future__ import absolute_import
from __future__ import unicode_literals

# pyborru imports
from .api import ApiFunctionsMixin
from .exceptions import PybooruError
from .resources import (API_BASE_URL, SITE_LIST)

# requests imports
import requests

# hashlib imports
import hashlib

# re imports
import re


class Pybooru(ApiFunctionsMixin, object):
    """Pybooru main class.

    To initialize Pybooru, you need to specify one of these two
    parameters: site_name or site_url. If you specify site_name, Pybooru checks
    whether there is in the list of default sites (You can get list of sites in
    the resources module).

    To specify a site that isn't in list of default sites, you need use site_url
    parameter.

    Some actions may require you to log in. always specify three parameters to
    log in: hash_string, username and password. Default sites has an associate
    hash string.

    Init Parameters:
        site_name (Type STR):
            The site name in SITE_LIST, default sites.

        site_url (Type STR):
            URL of based on Danbooru/Moebooru sites.

        hash_string (Type STR):
            String that is hashed (required to login).
            (See the API documentation of the site for more information).

        username (Type STR):
            Your username of the site
            (Required only for functions that modify the content).

        password (Type STR):
            Your user password in plain text
            (Required only for functions that modify the content).

    Attributes:
        site_name: Return site name.
        site_url: Return URL of based danbooru/Moebooru site.
        username: Return user name.
        password: Return password in plain text.
        hash_string: Return hash_string.
    """

    def __init__(self, site_name="", site_url="", username="", password="",
                 hash_string=""):

        # Attributes
        self.site_name = site_name.lower()
        self.site_url = site_url.lower()
        self.username = username
        self.password = password
        self.hash_string = hash_string

        # Validate site_name or site_url
        if site_url is not "" or site_name is not "":
            if site_name is not "":
                self._site_name_validator(self.site_name)
            elif site_url is not "":
                self._url_validator(self.site_url)
        else:
            raise PybooruError("Unexpected empty strings,"
                               " specify parameter site_name or site_url.")

    def _site_name_validator(self, site_name):
        """Function that checks the site name and get the url.

        Parameters:
            site_name (Type STR):
                The name of a based Danbooru/Moebooru site. You can get list
                of sites in the resources module.
        """
        if site_name in list(SITE_LIST.keys()):
            self.site_url = SITE_LIST[site_name]['url']
        else:
            raise PybooruError(
                "The site name is not valid, use the site_url parameter")

    def _url_validator(self, url):
        """URL validator for site_url parameter of Pybooru.

        Parameters:
            url (Type STR):
                The URL to validate.
        """
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
        if re.match('^(?:http|https)://', url):
            if re.search(regex, url):
                self.site_url = url
            else:
                raise PybooruError("Invalid URL", url=url)
        else:
            raise PybooruError("Invalid URL scheme, use HTTP or HTTPS", url=url)

    def _build_request_url(self, api_name, params=None):
        """Function for build url.

        Parameters:
            api_name:
                The NAME of the API function.

            params (Default: None):
                The parameters of the API function.
        """
        if params is None:
            params = {}

        # Create url
        url = self.site_url + API_BASE_URL[api_name]['url']

        # Build AUTENTICATION hash_string
        # Check if hash_string exists
        if API_BASE_URL[api_name]['required_login'] is True:
            if self.site_name in list(SITE_LIST.keys()) or \
                    self.hash_string is not "":

                # Check if the username and password are empty
                if self.username is not "" and self.password is not "":
                    # Set username login parameter
                    params['login'] = self.username

                    # Create hashed string
                    if self.hash_string is not "":
                        try:
                            hash_string = self.hash_string.format(self.password)
                        except TypeError:
                            raise PybooruError(r"Use \{0\} in hash_string")
                    else:
                        hash_string = SITE_LIST[self.site_name]['hashed_string'].format(self.password)

                    # Set password_hash parameter
                    # Convert hashed_string to SHA1 and return hex string
                    params['password_hash'] = hashlib.sha1(  # pylint: disable=E1101
                        hash_string).hexdigest()
                else:
                    raise PybooruError("Specify the username and password "
                                       "parameter of the Pybooru object, for "
                                       "setting password_hash attribute.")
            else:
                raise PybooruError(
                    "Specify the hash_string parameter of the Pybooru"
                    " object, for the functions which require login.")

        return self._json_request(url, params)

    @staticmethod
    def _json_request(url, params):
        """Function to read and returning JSON response.

        Parameters:
            url:
                API function url.

            params:
                API function parameters.
        """
        # Header
        headers = {'content-type': 'application/json; charset=utf-8'}

        try:
            # Request
            response = requests.post(url, params=params, headers=headers,
                                     timeout=60)
            # Enable raise status error
            response.raise_for_status()
            # Read and return JSON data
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise PybooruError("In _json_request", response.status_code,
                               response.url)
        except requests.exceptions.Timeout as err:
            raise PybooruError("Timeout! in url: {0}".format(response.url))
        except ValueError as err:
            raise PybooruError("JSON Error: {0} in line {1} column {2}".format(
                err.msg, err.lineno, err.colno))
