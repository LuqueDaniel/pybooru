# -*- coding: utf-8 -*-

"""pybooru.pybooru

This module contains pybooru main class for access to API calls,
authentication and return JSON response.

Classes:
   _Pybooru -- Main pybooru classs, define Pybooru object and do requests.
"""

# __furute__ imports
from __future__ import absolute_import

# External imports
import re
import requests

# pybooru imports
from . import __version__
from .exceptions import (PybooruError, PybooruHTTPError)
from .resources import (SITE_LIST, HTTP_STATUS_CODE)


class _Pybooru(object):
    """Pybooru main class.

    Attributes:
        site_name (str): Get or set site name set.
        site_url (str): Get or set the URL of Moebooru/Danbooru based site.
        username (str): Return user name.
        last_call (dict): Return last call.
    """

    def __init__(self, site_name='', site_url='', username=''):
        """Initialize Pybooru.

        Keyword arguments:
            site_name (str): The site name in 'SITE_LIST', default sites.
            site_url (str): URL of on Moebooru/Danbooru based sites.
            username (str): Your username of the site (Required only for
                            functions that modify the content).

        Raises:
            PybooruError: When 'site_name' and 'site_url' are empty.
        """
        # Attributes
        self.__site_name = ''  # for site_name property
        self.__site_url = ''  # for site_url property
        self.username = username
        self.last_call = {}

        # Set HTTP Client
        self.client = requests.Session()
        headers = {'user-agent': 'Pybooru/{0}'.format(__version__),
                   'content-type': 'application/json; charset=utf-8'}
        self.client.headers = headers

        # Validate site_name or site_url
        if site_name is not '':
            self.site_name = site_name
        elif site_url is not '':
            self.site_url = site_url
        else:
            raise PybooruError("Unexpected empty arguments, specify parameter "
                               "'site_name' or 'site_url'.")

    @property
    def site_name(self):
        """Get or set site name.

        :getter: Return site name.
        :setter: Validate and set site name.
        :type: string
        """
        return self.__site_name

    @site_name.setter
    def site_name(self, site_name):
        """Function that sets and checks the site name and set url.

        Parameters:
            site_name (str): The site name in 'SITE_LIST', default sites.

        Raises:
            PybooruError: When 'site_name' isn't valid.
        """
        if site_name in SITE_LIST:
            self.__site_name = site_name
            self.__site_url = SITE_LIST[site_name]['url']
            # Only for Moebooru
            if 'api_version' and 'hashed_string' in SITE_LIST[site_name]:
                self.api_version = SITE_LIST[site_name]['api_version']
                self.hash_string = SITE_LIST[site_name]['hashed_string']
        else:
            raise PybooruError(
                "The 'site_name' is not valid, specify a valid 'site_name'.")

    @property
    def site_url(self):
        """Get or set site url.

        :getter: Return site url.
        :setter: Validate and set site url.
        :type: string
        """
        return self.__site_url

    @site_url.setter
    def site_url(self, url):
        """URL setter and validator for site_url property.

        Parameters:
            url (str): URL of on Moebooru/Danbooru based sites.

        Raises:
            PybooruError: When URL scheme or URL are invalid.
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
                self.__site_url = url
            else:
                raise PybooruError("Invalid URL: {0}".format(url))
        else:
            raise PybooruError(
                "Invalid URL scheme, use HTTP or HTTPS: {0}".format(url))

    @staticmethod
    def _get_status(status_code):
        """Get status message for status code.

        Parameters:
            status_code (int): HTTP status code.

        Returns:
            status message (str).
        """
        return "{0}, {1}".format(*HTTP_STATUS_CODE.get(
            status_code, ('Undefined', 'undefined')))

    def _request(self, url, api_call, request_args, method='GET'):
        """Function to request and returning JSON data.

        Parameters:
            url (str): Base url call.
            api_call (str): API function to be called.
            request_args (dict): All requests parameters.
            method (str): (Defauld: GET) HTTP method 'GET' or 'POST'

        Raises:
            PybooruHTTPError: HTTP Error.
            requests.exceptions.Timeout: When HTTP Timeout.
            ValueError: When can't decode JSON response.
        """
        try:
            if method != 'GET':
                # Reset content-type for data encoded as a multipart form
                self.client.headers.update({'content-type': None})
            response = self.client.request(method, url, **request_args)

            self.last_call.update({
                'API': api_call,
                'url': response.url,
                'status_code': response.status_code,
                'status': self._get_status(response.status_code),
                'headers': response.headers
                })

            if response.status_code in (200, 201, 202, 204):
                return response.json()
            else:
                raise PybooruHTTPError("In _request", response.status_code,
                                       response.url)
        except requests.exceptions.Timeout:
            raise PybooruError("Timeout! url: {0}".format(response.url))
        except ValueError as e:
            raise PybooruError("JSON Error: {0} in line {1} column {2}".format(
                e.msg, e.lineno, e.colno))
