# -*- coding: utf-8 -*-

"""pybooru.resources

This module contains all resources for pybooru.

SITE_LIST:
    Is a dict that contains various based Danbooru/Moebooru, default sites.
HTTP_STATUS_CODES:
    Is a dict that contains the http status code for Danbooru/Moebooru API.
"""


# Default SITE_LIST
SITE_LIST = {
    'konachan': {
        'url': "http://konachan.com",
        'hashed_string': "So-I-Heard-You-Like-Mupkids-?--{0}--"},
    'yandere': {
        'url': "https://yande.re",
        'hashed_string': "choujin-steiner--{0}--"}
    }


# HTTP_STATUS_CODES
HTTP_STATUS_CODES = {
    200: ("OK", "Request was successful"),
    403: ("Forbidden", "Access denied"),
    404: ("Not Found", "Not found"),
    420: ("Invalid Record", "Record could not be saved"),
    421: ("User Throttled", "User is throttled, try again later"),
    422: ("Locked", "The resource is locked and cannot be modified"),
    423: ("Already Exists", "Resource already exists"),
    424: ("Invalid Parameters", "The given parameters were invalid"),
    500: ("Internal Server Error", "Some unknown error occurred on the server"),
    503: ("Service Unavailable", "Server cannot currently handle the request")
    }
