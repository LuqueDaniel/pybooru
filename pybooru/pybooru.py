#!/usr/bin/env Python
#encoding: utf-8

"""
    This module contain pybooru object class.
"""

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
            params += '&tags=%s' % (tags)

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
        elif name is not None:
            params += "&name=%s" % (name)
        elif after_id is not None:
            params += '&after_id=%i' % (after_id)

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

    def artists_list(self, name=None, order=None, page=1):
        """Get a list of artists.

        Parameters:
            name: The name (or a fragment of the name) of the artist.
            order: Can be date or name (Default value: None).
            page: The page number.
        """

        params = 'page=%i' % (page)

        if name is not None:
            params += '&name=%s' % (name)
        if order is not None:
            params += '&order=%s' % (order)

        return self._build_url('artists_list', params)

    def comments_show(self, id_=None):
        """Get a specific comment.

        Parameters:
            id_: The id number of the comment to retrieve.
        """

        if id_ is not None:
            params = 'id=%i' % (id_)
            return self._build_url('comments_show', params)
        else:
            raise PybooruError('id_ attribute is empty')

    def wiki_list(self, query=None, order='title', limit=100, page=1):
        """This function retrieves a list of every wiki page.

        Parameters:
            query: A word or phrase to search for (Default: None).
            order: Can be: title, date (Default: title).
            limit: The number of pages to retrieve (Default: 100).
            page: The page number.
        """
        params = 'order=%s&limit=%i&page=%i' % (order, limit, page)

        if query is not None:
            params += '&query=%s' % (query)

        return self._build_url('wiki_list', params)

    def wiki_show(self, title=None, version=None):
        """Get a specific wiki page.

        Parameters:
            title: The title of the wiki page to retrieve.
            version: The version of the page to retrieve.
        """

        if title is not None:
            params = 'title=%s' % (title)
        else:
            raise PybooruError('title attribute is empty')

        if version is not None:
            params += '&version=%i' % (version)

        return self._build_url('wiki_show', params)

    def wiki_history(self, title=None):
        """Get history of specific wiki page.

        Parameters:
            title: The title of the wiki page to retrieve versions for.
        """

        if title is not None:
            params = 'title=%s' % (title)
            return self._build_url('wiki_history', params)
        else:
            raise PybooruError('title atribute is required')

    def notes_list(self, post_id=None):
        """Get note list

        Parameters:
            post_id: The post id number to retrieve notes for (Default: None).
        """

        if post_id is not None:
            params = 'post_id=%i' % (post_id)
            return self._build_url('notes_list', params)
        else:
            return self._build_url('notes_list')

    def notes_search(self, query=None):
        """Search specific note.

        Parameters:
            query: A word or phrase to search for.
        """

        if query is not None:
            params = 'query=%s' % (query)
            return self._build_url('notes_search', params)
        else:
            raise PybooruError('query attribute is empty')

    def notes_history(self, post_id=None, id_=None, limit=10, page=1):
        """Get history of notes.

        Parameters:
            post_id: The post id number to retrieve note versions for.
            id_: The note id number to retrieve versions for.
            limit: How many versions to retrieve (Default: 10).
            page: The note id number to retrieve versions for.
        """

        params = 'limit=%i&page=%i' % (limit, page)

        if post_id is not None:
            params += '&post_id=%i' % (post_id)
        elif id_ is not None:
            params += '&id=%i' % (post_id)

        return self._build_url('notes_history', params)

    def users_search(self, name=None, id_=None):
        """Search users. If you don't specify any parameters you'll
           get a listing of all users.

        Parameters:
            name: The name of the user.
            id_: The id number of the user.
        """

        if name is not None:
            params = 'name=%s' % (name)
            return self._build_url('users_search', params)
        elif id_ is not None:
            params = 'id=%i' % (id_)
            return self._build_url('users_search', params)
        else:
            return self._build_url(self.users_url)

    def forum_list(self, id_=None):
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
