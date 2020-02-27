# -*- coding: utf-8 -*-

"""pybooru.resources

This module contains all resources for Pybooru.

SITE_LIST (dict):
    Contains various Moebooru and Danbooru-based default sites.
HTTP_STATUS_CODE (dict):
    Contains http status codes for Moebooru and Danbooru API.
"""


# Default SITE_LIST
SITE_LIST = {
    'konachan': {
        'url': "https://konachan.com",
        'api_version': "1.13.0+update.3",
        'hashed_string': "So-I-Heard-You-Like-Mupkids-?--{0}--"},
    'yandere': {
        'url': "https://yande.re",
        'api_version': "1.13.0+update.3",
        'hashed_string': "choujin-steiner--{0}--"},
    'danbooru': {
        'url': "https://danbooru.donmai.us"},
    'safebooru': {
        'url': "https://safebooru.donmai.us"},
    'lolibooru': {
        'url': "https://lolibooru.moe"},
    }


# HTTP_STATUS_CODE
HTTP_STATUS_CODE = {
    200: ("OK", "Request was successful"),
    201: ("Created", "The request has been fulfilled, resulting in the creation"
          " of a new resource"),
    202: ("Accepted", "The request has been accepted for processing, but the "
          "processing has not been completed."),
    204: ("No Content", "The server successfully processed the request and is "
          "not returning any content."),
    400: ("Bad request", "The server cannot or will not process the request"),
    401: ("Unauthorized", "Authentication is required and has failed or has "
          "not yet been provided."),
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
