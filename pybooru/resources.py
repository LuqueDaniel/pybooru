# -*- coding: utf-8 -*-

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
