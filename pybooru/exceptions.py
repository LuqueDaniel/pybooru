# -*- coding: utf-8 -*-

"""pybooru.exceptions

This module contains Pybooru exceptions.

Classes:
    PybooruError -- Main Pybooru exception class.
    PybooruHTTPError -- Manages HTTP status errors.
"""

# __furute__ imports
from __future__ import absolute_import
from __future__ import unicode_literals

# pybooru imports
from .resources import HTTP_STATUS_CODES


class PybooruError(Exception):
    """Class to return Pybooru error message."""
    pass


class PybooruHTTPError(PybooruError):
    """Class to return HTTP error message."""

    def __init__(self, msg, http_code, url):
        """Initialize PybooruHTTPError.

        Keyword arguments::
            msg: The error message.
            http_code: The HTTP status code.
            url: The URL.
        """

        if http_code in HTTP_STATUS_CODES and url is not None:
            msg = "{0}: {1} - {2}, {3} - URL: {4}".format(msg, http_code,
                        HTTP_STATUS_CODES[http_code][0],
                        HTTP_STATUS_CODES[http_code][1], url)

        super(PybooruHTTPError, self).__init__(msg)
