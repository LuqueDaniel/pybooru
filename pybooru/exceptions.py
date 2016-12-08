# -*- coding: utf-8 -*-

"""pybooru.exceptions

This module contains Pybooru exceptions.

Classes:
    * PybooruError -- Main Pybooru exception class.
    * PybooruHTTPError -- Manages HTTP status errors.
    * PybooruAPIError -- Manages all API errors.
"""

# __furute__ imports
from __future__ import absolute_import

# pybooru imports
from .resources import HTTP_STATUS_CODE


class PybooruError(Exception):
    """Class to catch Pybooru error message."""
    pass


class PybooruHTTPError(PybooruError):
    """Class to catch HTTP error message."""

    def __init__(self, msg, http_code, url):
        """Initialize PybooruHTTPError.

        Keyword arguments:
            :param msg: The error message.
            :param http_code: The HTTP status code.
            :param url: The URL.
        """
        super(PybooruHTTPError, self).__init__(msg, http_code, url)
        if http_code in HTTP_STATUS_CODE and url is not None:
            msg = "{0}: {1} - {2}, {3} - URL: {4}".format(
                msg, http_code, HTTP_STATUS_CODE[http_code][0],
                HTTP_STATUS_CODE[http_code][1], url)


class PybooruAPIError(PybooruError):
    """Class to catch all API errors."""
    pass
