# -*- coding: utf-8 -*-

"""This module contains the exceptions."""

# __furute__ imports
from __future__ import absolute_import
from __future__ import unicode_literals

# pybooru imports
from .resources import HTTP_STATUS_CODES


class PybooruError(Exception):
    """Class to return error message.

    Init Parameters:
        msg:
            The error message.

        http_code:
            The HTTP status code.

        url:
            The URL.

    Attributes:
        msg: Return the error message.
        http_code: Return the HTTP status code.
        url: return the URL.
    """

    def __init__(self, msg, http_code=None, url=None):
        super(PybooruError, self).__init__()

        self.msg = msg
        self.http_code = http_code
        self.url = url

        if http_code in HTTP_STATUS_CODES and self.url is not None:
            self.msg = "{0}: {1}, {2} - {3} -- URL: {4}".format(self.msg,
                            http_code, HTTP_STATUS_CODES[http_code][0],
                            HTTP_STATUS_CODES[http_code][1], self.url)

    def __str__(self):
        """Function to return error message."""
        return repr(self.msg)

    def __repr__(self):
        """Function to return self.msg repr."""
        return self.msg
