#!/usr/bin/env Python
#encoding: utf-8

"""
    Pybooru is a library for Python for access to API Danbooru based sites.

    Under a MIT License
"""

__author__ = 'Daniel Luque <danielluque14 at gmail.com>'
__version__ = '1.4.9'


#urllib2 imports
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError

#urlparse imports
from urlparse import urlparse

try:
    #simplejson imports
    from simplejson import loads
except ImportError:
    try:
        #Python 2.6 and up
        from json import loads
    except ImportError:
        raise Exception('Pybooru requires the simplejson library to work')

#pyborru resources imports
from resources import http_status_codes
from resources import site_list


class PybooruError(Exception):
    """Class for return error message

    init Parameters:
        msg: The error message
        http_code: The HTTP status code
        url: The URL

    Attributes:
        msg: Return the error message
        http_code: Return the HTTP status code
        url: return the URL
    """

    def __init__(self, msg, http_code=None, url=None):
        self.msg = msg
        self.http_code = http_code
        self.url = url

        if (http_code is not None) and (http_code in http_status_codes) and (
            url is not None):
            self.msg = '%i: %s, %s -- %s -- URL: %s' % (http_code,
                        http_status_codes[http_code][0],
                        http_status_codes[http_code][1], self.msg, url)

    def __str__(self):
        """This function return self.msg"""

        return repr(self.msg)


class Pybooru(object):
    """Pybooru class

    init Parameters:
        siteName: The site name in site_list
        siteURL: URL of based Danbooru site

    Attributes:
        siteName: Return site name
        siteURL: Return URL of based danbooru site
    """

    def __init__(self, siteName=None, siteURL=None):
        self.siteName = siteName
        self.siteURL = siteURL

        if not (self.siteURL is not None) and (self.siteName is not None):
            if self.siteName is not None:
                self._site_name(self.siteName.lower())
            elif self.siteURL is not None:
                self._url_validator(self.siteURL.lower())
        else:
            raise PybooruError('siteURL and siteName are None')

    def _site_name(self, siteName):
        """Function for check name site and get URL

        Parameters:
          siteName: The name of a based Danbooru site. You can get list of sites
                    in the resources module.
        """

        if siteName in site_list.keys():
            self.siteURL = site_list[siteName]
        else:
            raise PybooruError(
                        'The site name is not valid, use siteURL parameter'
                        )

    def _url_validator(self, url):
        """URL validator for siteURL parameter of Pybooru

        Parameters:
            url: The URL to validate
        """

        #urlparse() from urlparse module
        parse = urlparse(url)

        if parse.scheme not in ('http', 'https'):
            if parse.scheme == '':
                url = 'http://' + parse.path
            else:
                url = 'http://' + parse.netloc

        self.siteURL = url

    def _build_url(self, api_url, params=None):
        """Builder url for _json_load

        Parameters:
            api_url: The URL of the API function
            params: The parameters of the API function
        """

        if params is not None:
            self.url_request = self.siteURL + api_url + params
            self.url_request = self._json_load(self.url_request)
            return self.url_request
        else:
            self.url_request = self.siteURL + api_url
            self.url_request = self._json_load(self.url_request)
            return self.url_request

    def _json_load(self, url):
        """Function for read and return JSON response

        Parameters:
            url: The url for JSON request
        """

        try:
            #urlopen() from module urllib2
            self.openURL = urlopen(url)
            self.reading = self.openURL.read()
            #loads() is a function of simplejson module
            self.response = loads(self.reading)
            return self.response
        except (URLError, HTTPError) as err:
            if hasattr(err, 'code'):
                raise PybooruError('in _json_load', err.code, url)
            else:
                raise PybooruError('in _json_load %s' % (err.reason), url)
        except ValueError as err:
            raise PybooruError('JSON Error: %s in line %s column %s' % (
                               err.msg, err.lineno, err.colno))

    def posts(self, tags=None, limit=10, page=1):
        self.posts_url = '/post/index.json?'
        self.params = 'limit=%i&page=%i' % (limit, page)

        if tags is not None:
            self.tags = str(tags)
            self.params += '&tags=%s' % (tags)
            return self._build_url(self.posts_url, self.params)
        else:
            return self._build_url(self.posts_url, self.params)

    def tags(self, name=None, id_=None, limit=100, page=1, order='name',
                                                            after_id=0):
        self.tags_url = '/tag/index.json?'

        if id_ is not None:
            self.params = 'id=%i' % (id_)
            return self._build_url(self.tags_url, self.params)
        if name is not None:
            self.name = str(name)
            self.params = "name=%s" % (self.name)
            return self._build_url(self.tags_url, self.params)
        else:
            self.params = "limit=%i&page=%i&order=%s&after_id=%i" % (limit,
                                                    page, order, after_id)
            return self._build_url(self.tags_url, self.params)

    def artists(self, name=None, id_=None, limit=20, order='name', page=1):
        self.artists_url = '/artist/index.json?'
        self.params = 'limit=%i&page%i&order=%s' % (limit, page, order)

        if name is not None:
            self.name = str(name)
            self.params += '&name=%s' % (self.name)
            return self._build_url(self.artists_url, self.params)
        elif id_ is not None:
            self.params = 'id=%i' % (id_)
            return self._build_url(self.artists_url, self.params)
        else:
            return self._build_url(self.artists_url, self.params)

    def comments(self, id_=None):
        self.comments_url = '/comment/show.json?'

        if id_ is not None:
            self.params = 'id=%i' % (id_)
            return self._build_url(self.comments_url, self.params)
        else:
            print PybooruError('id_ attribute is empty')

    def wiki(self, query=None, order='title', limit=20, page=1):
        self.wiki_url = '/wiki/index.json?'
        self.params = 'order=%s&limit=%i&page=%i' % (order, limit, page)

        if query is not None:
            self.query = str(query)
            self.params += '&query=%s' % (self.query)
            return self._build_url(self.wiki_url, self.params)
        else:
            return self._build_url(self.wiki_url, self.params)

    def wiki_history(self, title=None):
        self.wiki_history_url = '/wiki/history.json?'

        if title is not None:
            self.title = str(title)
            self.params = 'title=%s' % (self.title)
            return self._build_url(self.wiki_history_url, self.params)
        else:
            raise PybooruError('title atribute is required')

    def notes(self, id_=None):
        self.notes_url = '/note/index.json?'

        if id_ is not None:
            self.params = 'post_id=%i' % (id_)
            return self._build_url(self.notes_url, self.params)
        else:
            return self._build_url(self.notes_url)

    def search_notes(self, query=None):
        self.search_notes_url = '/note/search.json?'

        if query is not None:
            self.query = str(query)
            self.params = 'query=%s' % (self.query)
            return self._build_url(self.search_notes_url, self.params)
        else:
            raise PybooruError('query attribute is empty')

    def history_notes(self, post_id=None, id_=None, limit=10, page=1):
        self.history_notes_url = '/note/history.json?'

        if post_id is not None:
            self.params = 'post_id=%i' % (post_id)
            return self._build_url(self.history_notes_url, self.params)
        elif id_ is not None:
            self.params = 'id=%i' % (post_id)
            return self._build_url(self.history_notes_url, self.params)
        else:
            self.params = 'limit=%i&page=%i' % (limit, page)
            return self._build_url(self.history_notes_url, self.params)

    def users(self, name=None, id_=None):
        self.users_url = '/user/index.json?'

        if name is not None:
            self.name = str(name)
            self.params = 'name=%s' % (self.name)
            return self._build_url(self.users_url, self.params)
        elif id_ is not None:
            self.params = 'id=%i' % (self.id_)
            return self._build_url(self.users_url, self.params)
        else:
            return self._build_url(self.users_url)

    def forum(self, id_=None):
        self.forum_url = '/forum/index.json?'

        if id_ is not None:
            self.params = 'parent_id%i' % (id_)
            return self._build_url(self.forum_url, self.params)
        else:
            return self._build_url(self.forum_url)

    def pools(self, query=None, page=1):
        self.pools_url = '/pool/index.json?'

        if query is not None:
            self.query = str(query)
            self.params = 'query=%s' % (self.query)
            return self._build_url(self.pools_url, self.params)
        else:
            self.params = 'page=%i' % (page)
            return self._build_url(self.pools_url, self.params)

    def pools_posts(self, id_=None, page=1):
        self.pools_posts_url = '/pool/show.json?'

        if id_ is not None:
            self.params = 'id=%i&page=%i' % (id_, page)
            return self._build_url(self.pools_posts_url, self.params)
        else:
            raise PybooruError('id_ attribute is empty')

    def favorites(self, id_=None):
        self.favorites = '/favorite/list_users.json?'

        if id_ is not None:
            self.params = 'id=%i' % (id_)
            return self._build_url(self.favorites, self.params)
        else:
            raise PybooruError('id_ attribute is empty')

    def tag_history(self, post_id=None, user_id=None, user_name=None):
        self.tag_history_url = '/post_tag_history/index.json?'

        if post_id is not None:
            self.params = 'post_id=%i' % (post_id)
            return self._build_url(self.tag_history_url, self.params)
        if user_id is not None:
            self.params = 'user_id=%i' % (user_id)
            return self._build_url(self.tag_history_url, self.params)
        if user_name is not None:
            self.user_name = str(user_name)
            self.params = 'user_name=%s' % (self.user_name)
            return self._build_url(self.tag_history_url, self.params)


if __name__ == '__main__':
    raise PybooruError('Import this module into your project to use')
