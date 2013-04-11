# -*- coding: utf-8 -*-

"""
    This module contain all resources for pybooru

    site_list: Is a dict contains various based Danbooru default sites
    http_status_codes: Is a dict contains the http status code for Danbooru API
"""

#site_list
site_list = {'konachan': 'http://konachan.com',
             'danbooru': 'http://danbooru.donmai.us',
             'yandere': 'https://yande.re',
             'chan-sankaku': 'http://chan.sankakucomplex.com',
             'idol-sankaku': 'http://idol.sankakucomplex.com',
             '3dbooru': 'http://behoimi.org'}

#http_status_codes
http_status_codes = {
    200: ('OK', 'Request was successful'),
    403: ('Forbidden', 'Access denied'),
    404: ('Not Found', 'Not found'),
    420: ('Invalid Record', 'Record could not be saved'),
    421: ('User Throttled', 'User is throttled, try again later'),
    422: ('Locked', 'The resource is locked and cannot be modified'),
    423: ('Already Exists', 'Resource already exists'),
    424: ('Invalid Parameters', 'The given parameters were invalid'),
    500: ('Internal Server Error', 'Some unknown error occurred on the server'),
    503: ('Service Unavailable', 'Server cannot currently handle the request')
    }
