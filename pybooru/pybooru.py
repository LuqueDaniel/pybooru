#!/usr/bin/env Python
#encoding: utf-8


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
from .exceptions import PybooruError
from .resources import api_base_url
from .resources import site_list


class Pybooru(object):
    """Pybooru class.

    init Parameters:
        siteName: The site name in site_list.
        siteURL: URL of based Danbooru site.

    Attributes:
        siteName: Return site name.
        siteURL: Return URL of based danbooru site.
    """

    def __init__(self, siteName=None, siteURL=None):
        self.siteName = siteName
        self.siteURL = siteURL

        if (siteURL is not None) or (siteName is not None):
            if type(siteName) is str:
                self._site_name(siteName.lower())
            elif type(siteURL) is str:
                self._url_validator(siteURL.lower())
            else:
                raise PybooruError('Expected type str for siteName and siteURL')
        else:
            raise PybooruError('siteName and siteURL are None')

    def _site_name(self, siteName):
        """Function for checking name site and get URL.

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
        """URL validator for siteURL parameter of Pybooru.

        Parameters:
            url: The URL to validate.
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
        """Builder url for _json_load.

        Parameters:
            api_url: The URL of the API function.
            params: The parameters of the API function.
        """

        if params is not None:
            url_request = self.siteURL + api_base_url[api_url] + params
            url_request = self._json_load(url_request)
            return url_request
        else:
            url_request = self.siteURL + api_base_url[api_url]
            url_request = self._json_load(url_request)
            return url_request

    def _json_load(self, url):
        """Function for reading and returning JSON response.

        Parameters:
            url: The url for JSON request.
        """

        try:
            #urlopen() from module urllib2
            openURL = urlopen(url)
            reading = openURL.read()
            #loads() is a function of simplejson module
            response = loads(reading)
            return response
        except (URLError, HTTPError) as err:
            if hasattr(err, 'code'):
                raise PybooruError('in _json_load', err.code, url)
            else:
                raise PybooruError('in _json_load %s' % (err.reason), url)
        except ValueError as err:
            raise PybooruError('JSON Error: %s in line %s column %s' % (
                               err.msg, err.lineno, err.colno))

    def posts_list(self, tags=None, limit=100, page=1):
        """Get a list of posts.

        Parameters:
            tags: The tags of the posts (Default: None).
            limit: Limit of posts. Limit of 100 posts per request
                   (Default: 100).
            page: The page number (Default: 1).
        """

        params = 'limit=%i&page=%i' % (limit, page)

        if tags is not None:
            params += '&tags=%s' % (str(tags))
            return self._build_url('posts_list', params)
        else:
            return self._build_url('posts_list', params)

    def tags_list(self, name=None, id_=None, limit=0, page=1, order='name',
                  after_id=None):
        """Get a list of tags.

        Parameters:
            name: The exact name of the tag.
            id_: The id number of the tag.
            limit: How many tags to retrieve. Setting this to 0 will return
                   every tag (Default value: 0).
            page: The page number.
            order: Can be 'date', 'name' or 'count' (Default: name).
            after_id: Return all tags that have an id number greater than this.
        """

        params = 'limit=%i&page=%i&order=%s' % (limit, page, order)

        if id_ is not None:
            params += '&id=%i' % (id_)
            return self._build_url('tags_list', params)
        elif name is not None:
            params += "&name=%s" % (str(name))
            return self._build_url('tags_list', params)
        elif after_id is not None:
            params += '&after_id=%i' % (after_id)
            return self._build_url('tags_list', params)
        else:
            return self._build_url('tags_list', params)

    def tags_related(self, tags, type_=None):
        """Get a list of related tags.

        Parameters:
            tags: The tag names to query.
            type_: Restrict results to this tag type. Can be general, artist,
                   copyright, or character (Default value: None).
        """

        params = 'tags=%s' % (tags)

        if type_ is not None:
            params += '&type=%s' % (type_)
            return self._build_url('tags_related', params)
        else:
            return self._build_url('tags_related', params)

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
            raise PybooruError('id_ attribute is empty')

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
