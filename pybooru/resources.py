"""
    This module contain all resources for pybooru.

    site_list: Is a dict contains various based Danbooru default sites.
    api_base_url: Is a dict contain the urls for API functions.
    http_status_codes: Is a dict contains the http status code for Danbooru API.
"""

#site_list
site_list = {
             'konachan': {
                 'url': 'http://konachan.com',
                 'hashed_string': 'So-I-Heard-You-Like-Mupkids-?--%s--'},

             'yandere': {
                 'url': 'https://yande.re',
                 'hashed_string': 'choujin-steiner--%s--'}
            }


#api_base_url for the API functions
api_base_url = {
    'posts_list': {
        'url': '/post.json',
        'required_login': False},
    'posts_revert_tags': {
        'url': '/post/revert_tags.json',
        'required_login': True},
    'posts_vote': {
        'url': '/post/vote.json',
        'required_login': True},
    'tags_list': {
        'url': '/tag.json',
        'required_login': False},
    'tags_update': {
        'url': '/tag/update.json',
        'required_login': True},
    'tags_related': {
        'url': '/tag/related.json',
        'required_login': False},
    'artists_list': {
        'url': '/artist.json',
        'required_login': False},
    'artists_destroy': {
        'url': '/artist/destroy.json',
        'required_login': True},
    'comments_show': {
        'url': '/comment/show.json',
        'required_login': False},
    'comments_create': {
        'url': '/comment/create.json',
        'required_login': True},
    'comments_destroy': {
        'url': '/comment/destroy.json',
        'required_login': True},
    'wiki_list': {
        'url': '/wiki.json',
        'required_login': False},
    'wiki_create': {
        'url': '/wiki/create.json',
        'required_login': True},
    'wiki_update': {
        'url': '/wiki/update.json',
        'required_login': True},
    'wiki_show': {
        'url': '/wiki/show.json',
        'required_login': False},
    'wiki_destroy': {
        'url': '/wiki/destroy.json',
        'required_login': True},
    'wiki_lock': {
        'url': '/wiki/lock.json',
        'required_login': True},
    'wiki_unlock': {
        'url': '/wiki/unlock.json',
        'required_login': True},
    'wiki_revert': {
        'url': '/wiki/revert.json',
        'required_login': True},
    'wiki_history': {
        'url': '/wiki/history.json',
        'required_login': False},
    'notes_list': {
        'url': '/note.json',
        'required_login': False},
    'notes_search': {
        'url': '/note/search.json',
        'required_login': False},
    'notes_history': {
        'url': '/note/history.json',
        'required_login': False},
    'users_search': {
        'url': '/user.json',
        'required_login': False},
    'forum_list': {
        'url': '/forum.json',
        'required_login': False},
    'pools_list': {
        'url': '/pool.json',
        'required_login': False},
    'pools_posts': {
        'url': '/pool/show.json',
        'required_login': False},
    'favorites_list_users': {
        'url': '/favorite/list_users.json',
        'required_login': False}
    }


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
