"""
    This module contain pybooru object class.
"""

#urllib2 imports
from urllib import urlencode
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError

#urlparse imports
from urlparse import urlparse

#hashlib imports
import hashlib

try:
    #simplejson imports
    from simplejson import loads
except ImportError:
    try:
        #Python 2.6 and up
        from json import loads
    except ImportError:
        raise Exception('Pybooru requires the simplejson library to work')

#pyborru exceptions imports
from .exceptions import PybooruError
#pybooru resources imports
from .resources import api_base_url
from .resources import site_list


class Pybooru(object):
    """Pybooru class.

    init Parameters:
        siteName: The site name in site_list.
        siteURL: URL of based Danbooru site.
        username: Your username in site
                  (Required only for functions that modify the content).
        password: Your user password
                  (Required only for functions that modify the content).

    Attributes:
        siteName: Return site name.
        siteURL: Return URL of based danbooru site.
        username: Return user name.
        password: Return password.
    """

    def __init__(self, siteName=None, siteURL=None, username=None,
                 password=None):

        self.siteName = siteName
        self.siteURL = siteURL
        self.username = username
        self.password = password

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
            self.siteURL = site_list[siteName]['url']
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

    def _json_load(self, api_name, params=None):
        """Function for reading and returning JSON response.

        Parameters:
            api_name: The NAME of the API function.
            params: The parameters of the API function.
        """

        url = self.siteURL + api_base_url[api_name]['url']

        #Autentication
        if api_base_url[api_name]['required_login'] is True:
            if self.siteName in site_list.keys():
                if (self.username is not None) and (self.password is not None):
                    #Set login parameter
                    params['login'] = self.username

                    #Create hashed string
                    has_string = site_list[self.siteName]['hashed_string'] % (
                                    self.password)

                    #Convert hashed_string to SHA1 and return hex string
                    params['password_hash'] = hashlib.sha1(
                                                has_string).hexdigest()

                else:
                    raise PybooruError('username and password is required')

            else:
                raise PybooruError('Login in %s unsupported' % self.siteName)

        #JSON request
        try:
            #urlopen() from module urllib2
            #urlencode() from module urllib
            openURL = urlopen(url, urlencode(params))
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

        params = {'limit': limit, 'page': page}

        if tags is not None:
            params['tags'] = tags

        return self._json_load('posts_list', params)

    def posts_revert_tags(self, id_, history_id):
        """This action reverts a post to a previous set of tags
           (Requires login)(UNTESTED).

        Parameters:
            id_: The post id number to update.
            history_id: The id number of the tag history.
        """

        if type(id_) is int and type(history_id) is int:
            params = {'id': id_, 'history_id': history_id}
            return self._json_load('posts_revert_tags', params)
        else:
            raise PybooruError('id_ and history_id is expected type int')

    def posts_vote(self, id_, score):
        """This action lets you vote for a post (Requires login).

        Parameters:
            id_: The post id.
            score: Be can:
                0: No voted or Remove vote.
                1: Good.
                2: Great.
                3: Favorite, add post to favorites.
        """

        if type(id_) is int and type(score) is int:
            if score <= 3:
                params = {'id': id_, 'score': score}
                return self._json_load('posts_vote', params)
            else:
                raise PybooruError('Value of score only can be 0, 1, 2 and 3.')
        else:
            raise PybooruError('id_ and score is expected type int')

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

        params = {'limit': limit, 'page': page, 'order': order}

        if id_ is not None:
            params['id'] = id_
        elif name is not None:
            params['name'] = name
        elif after_id is not None:
            params['after_id'] = after_id

        return self._json_load('tags_list', params)

    def tags_update(self, name, tag_type, is_ambiguous):
        """This action lets you update tag (Requires login)(UNTESTED)

        Parameters:
            name: The name of the tag to update.
            tag_type: The tag type.
                General: 0.
                artist: 1.
                copyright: 3.
                character: 4.
            is_ambiguous: Whether or not this tag is ambiguous.
                          Use 1 for true and 0 for false.
        """

        params = {'name': name, 'tag[tag_type]': tag_type,
                  'tag[is_ambiguous]': is_ambiguous}

        return self._json_load('tags_update', params)

    def tags_related(self, tags, type_=None):
        """Get a list of related tags.

        Parameters:
            tags: The tag names to query.
            type_: Restrict results to this tag type. Can be general, artist,
                   copyright, or character (Default value: None).
        """

        params = {'tags': tags}

        if type_ is not None:
            params['type'] = type_

        return self._json_load('tags_related', params)

    def artists_list(self, name=None, order=None, page=1):
        """Get a list of artists.

        Parameters:
            name: The name (or a fragment of the name) of the artist.
            order: Can be date or name (Default value: None).
            page: The page number.
        """

        params = {'page': page}

        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order

        return self._json_load('artists_list', params)

    def artists_destroy(self, id_):
        """This action lets you remove artist (Requires login).

        Parameters:
            id_: The id of the artist to destroy.
        """

        if type(id_) is int:
            return self._json_load('artists_destroy', {'id': id_})
        else:
            raise PybooruError('id_ is expected type int')

    def comments_show(self, id_):
        """Get a specific comment.

        Parameters:
            id_: The id number of the comment to retrieve.
        """

        if type(id_) is not int:
            params = {'id': id_}
            return self._json_load('comments_show', params)
        else:
            raise PybooruError('id_ is expected type int')

    def comments_create(self, post_id, comment_body):
        """This action lets you create a comment (Requires login).

        Parameters:
            post_id: The post id number to which you are responding.
            comment_body: The body of the comment.
        """

        if type(post_id) is int:
            params = {'comment[post_id]': post_id,
                      'comment[body]': comment_body}
            response = self._json_load('comments_create', params)
            return response['success']
        else:
            raise PybooruError('post_id is expected type int')

    def comments_destroy(self, id_=None):
        """Remove a specific comment (Requires login).

        Parameters:
            id_: The id number of the comment to remove.
        """

        if type(id_) is not int:
            params = {'id': id_}
            response = self._json_load('comments_destroy', params)
            return response['success']
        else:
            raise PybooruError('id_ is expected type int')

    def wiki_list(self, query=None, order='title', limit=100, page=1):
        """This function retrieves a list of every wiki page.

        Parameters:
            query: A word or phrase to search for (Default: None).
            order: Can be: title, date (Default: title).
            limit: The number of pages to retrieve (Default: 100).
            page: The page number.
        """

        params = {'order': order, 'limit': limit, 'page': page}

        if query is not None:
            params['query'] = query

        return self._json_load('wiki_list', params)

    def wiki_create(self, title, body):
        """This action lets yout create a wiki page (Requires login)(UNTESTED)

        Parameters:
            title: The title of the wiki page.
            body: The body of the wiki page.
        """

        params = {'wiki_page[title]': str(title), 'wiki_page[body]': str(body)}
        return self._json_load('wiki_create', params)

    def wiki_show(self, title=None, version=None):
        """Get a specific wiki page.

        Parameters:
            title: The title of the wiki page to retrieve.
            version: The version of the page to retrieve.
        """

        if title is not None:
            params = {'title': title}

            if version is not None:
                params['version'] = version

            return self._json_load('wiki_show', params)
        else:
            raise PybooruError('title parameter is required')

    def wiki_history(self, title=None):
        """Get history of specific wiki page.

        Parameters:
            title: The title of the wiki page to retrieve versions for.
        """

        if title is not None:
            params = {'title': title}
            return self._json_load('wiki_history', params)
        else:
            raise PybooruError('title atribute is required')

    def notes_list(self, post_id=None):
        """Get note list

        Parameters:
            post_id: The post id number to retrieve notes for (Default: None).
        """

        if post_id is not None:
            params = {'post_id': post_id}
            return self._json_load('notes_list', params)
        else:
            return self._json_load('notes_list')

    def notes_search(self, query=None):
        """Search specific note.

        Parameters:
            query: A word or phrase to search for.
        """

        if query is not None:
            params = {'query': query}
            return self._json_load('notes_search', params)
        else:
            raise PybooruError('query parameter is required')

    def notes_history(self, post_id=None, id_=None, limit=10, page=1):
        """Get history of notes.

        Parameters:
            post_id: The post id number to retrieve note versions for.
            id_: The note id number to retrieve versions for.
            limit: How many versions to retrieve (Default: 10).
            page: The note id number to retrieve versions for.
        """

        params = {'limit': limit, 'page': page}

        if post_id is not None:
            params['post_id'] = post_id
        elif id_ is not None:
            params['id'] = id_

        return self._json_load('notes_history', params)

    def users_search(self, name=None, id_=None):
        """Search users. If you don't specify any parameters you'll
           get a listing of all users.

        Parameters:
            name: The name of the user.
            id_: The id number of the user.
        """

        if name is not None:
            params = {'name': name}
            return self._json_load()('users_search', params)
        elif id_ is not None:
            params = {'id': id_}
            return self._json_load('users_search', params)
        else:
            return self._json_load('users_search')

    def forum_list(self, parent_id=None):
        """Get forum posts. If you don't specify any parameters you'll get
           a listing of all users.

        Parameters:
            parent_id: The parent ID number. You'll return all the responses to
                       that forum post.
        """

        if parent_id is not None:
            params = {'parent_id': parent_id}
            return self._json_load('forum_list', params)
        else:
            return self._json_load('forum_list')

    def pools_list(self, query=None, page=1):
        """Get pools. If you don't specify any parameters you'll get a
           list of all pools.

        Parameters:
            query: The title.
            page: The page.
        """

        params = {'page': page}

        if query is not None:
            params['query': query]

        return self._json_load('pools_list', params)

    def pools_posts(self, id_=None, page=1):
        """Get pools posts. If you don't specify any parameters you'll get a
           list of all pools.

        Parameters:
            id_: The pool id number.
            page: The page.
        """

        params = {'page': page}

        if id_ is not None:
            params['id'] = id_

        return self._json_load('pools_posts', params)

    def favorites_list_users(self, id_=None):
        """Return a list with all users who have added to favorites a specific
           post.

        Parameters:
            id_: The post id.
        """

        if id_ is not None:
            params = {'id': id_}
            response = self._json_load('favorites_list_users', params)
            #Return list with users
            return response['favorited_users'].split(',')
        else:
            raise PybooruError('id_ parameter is required')
