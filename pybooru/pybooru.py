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
        :var site_name: Return site name.
        :var site_url: Return the URL of Moebooru/Danbooru based site.
        :var username: Return user name.
        :var last_call: Return last call.
    """

    def __init__(self, site_name="", site_url="", username=""):
        """Initialize Pybooru.

        Keyword arguments:
            :param site_name: The site name in 'SITE_LIST', default sites.
            :param site_url: URL of on Moebooru/Danbooru based sites.
            :param username: Your username of the site (Required only for
                             functions that modify the content).
        """
        # Attributes
        self.site_name = site_name.lower()
        self.site_url = site_url.lower()
        if username is not "":
            self.username = username
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
            # Only for Moebooru
            if 'api_version' and 'hashed_string' in SITE_LIST[self.site_name]:
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
        """Get status message for status code"""
        if status_code in HTTP_STATUS_CODE:
            return "{0}, {1}".format(*HTTP_STATUS_CODE[status_code])
        else:
            return None

    def _request(self, url, api_call, request_args, method='GET'):
        """Function to request and returning JSON data.

        Parameters:
            :param url: Base url call.
            :param api_call: API function to be called.
            :param request_args: All requests parameters.
            :param method: (Defauld: GET) HTTP method 'GET' or 'POST'

        :raises requests.exceptions.Timeout: When HTTP Timeout.
        :raises ValueError: When can't decode JSON response.
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
            raise PybooruError("Timeout! in url: {0}".format(response.url))
        except ValueError as e:
            raise PybooruError("JSON Error: {0} in line {1} column {2}".format(
                e.msg, e.lineno, e.colno))
