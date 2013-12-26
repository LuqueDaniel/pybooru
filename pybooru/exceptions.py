"""This module contain the exceptions."""

# pybooru impost
from .resources import HTTP_STATUS_CODES


class PybooruError(Exception):
    """Class for returning error message.

    init Parameters:
        msg:
            The error message.

        http_code:
            The HTTP status code.

        url:
            The URL.

    Attributes:
        msg -- Return the error message.
        http_code -- Return the HTTP status code.
        url -- return the URL.
    """

    def __init__(self, msg, http_code=None, url=None):
        self.msg = msg
        self.http_code = http_code
        self.url = url

        if (http_code is not None) and (http_code in HTTP_STATUS_CODES) and (
            url is not None):
            self.msg = '%i: %s, %s -- %s -- URL: %s' % (http_code,
                        HTTP_STATUS_CODES[http_code][0],
                        HTTP_STATUS_CODES[http_code][1], self.msg, url)

    def __str__(self):
        """This function return self.msg"""

        return repr(self.msg)
