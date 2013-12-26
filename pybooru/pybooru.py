# -*- coding: utf-8 -*-

"""This module contain pybooru object class."""

# urllib2 imports
from urllib import urlencode
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError

# urlparse imports
from urlparse import urlparse

# hashlib imports
import hashlib

try:
    # simplejson imports
    from simplejson import loads
except ImportError:
    try:
        # Python 2.6 and up
        from json import loads
    except ImportError:
        raise Exception('Pybooru requires the simplejson library to work')

# pyborru exceptions imports
from .exceptions import PybooruError
# pybooru resources imports
from .resources import API_BASE_URL
from .resources import SITE_LIST


class Pybooru(object):
    """Pybooru class.

    init Parameters:
        siteName:
            The site name in SITE_LIST.

        siteURL:
            URL of based Danbooru site.

        username:
            Your username in site
            (Required only for functions that modify the content).

        password:
            Your user password in plain text.
            (Required only for functions that modify the content).

        hashString:
            string that is hashed.
            (See the API of the site for more information).

    Attributes:
        siteName -- Return site name.
        siteURL -- Return URL of based danbooru site.
        username -- Return user name.
        password -- Return password in plain text.
        hashString -- Return hashString.
    """

    def __init__(self, siteName=None, siteURL=None, username=None,
                 password=None, hashString=None):

        self.siteName = siteName
        self.siteURL = siteURL
        self.username = username
        self.password = password
        self.hashString = hashString

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
          :siteName:
              The name of a based Danbooru site. You can get list of sites
              in the resources module.
        """

        if siteName in SITE_LIST.keys():
            self.siteURL = SITE_LIST[siteName]['url']
        else:
            raise PybooruError(
                        'The site name is not valid, use siteURL parameter'
                        )

    def _url_validator(self, url):
        """URL validator for siteURL parameter of Pybooru.

        Parameters:
            :url:
                The URL to validate.
        """

        # urlparse() from urlparse module
        parse = urlparse(url)

        if parse.scheme not in ('http', 'https'):
            if parse.scheme == '':
                url = 'http://' + parse.path
            else:
                url = 'http://' + parse.netloc

        self.siteURL = url

    def _json_load(self, api_name, params=None):
        """Function for read and return JSON response.

        Parameters:
            :api_name:
                The NAME of the API function.

            :params:
                The parameters of the API function.
        """

        url = self.siteURL + API_BASE_URL[api_name]['url']

        # Autentication
        if API_BASE_URL[api_name]['required_login'] is True:
            if (self.siteName in SITE_LIST.keys()) or (self.hashString is not None):
                if (self.username is not None) and (self.password is not None):
                    # Set login parameter
                    params['login'] = self.username

                    # Create hashed string
                    if self.hashString is not None:
                        try:
                            has_string = self.hashString % (self.password)
                        except TypeError:
                            raise PybooruError('Use "%s" for hashString')
                    else:
                        has_string = SITE_LIST[self.siteName]['hashed_string'] % (
                                        self.password)

                    # Set password_hash parameter
                    # Convert hashed_string to SHA1 and return hex string
                    params['password_hash'] = hashlib.sha1(
                                                has_string).hexdigest()

                else:
                    raise PybooruError('username and password is required')

            else:
                raise PybooruError('Login in %s unsupported, please use hashString' % self.siteName)

        # JSON request
        try:
            if params is not None:
                # urlopen() from module urllib2
                # urlencode() from module urllib
                openURL = urlopen(url, urlencode(params))
            else:
                openURL = urlopen(url)

            reading = openURL.read()
            # loads() is a function of simplejson module
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
            :tags:
                The tags of the posts (Default: None).

            :limit:
                Limit of posts. Limit of 100 posts per request (Default: 100).

            :page:
                The page number (Default: 1).
        """

        params = {'limit': limit, 'page': page}

        if tags is not None:
            params['tags'] = tags

        return self._json_load('posts_list', params)

    def posts_create(self, tags, file_=None, rating=None, source=None,
                     is_rating_locked=None, is_note_locked=None,
                     parent_id=None, md5=None):
        """This function create a new post. There are only two mandatory
        fields: you need to supply the tags, and you need to supply the
        file, either through a multipart form or through a source URL.
        (Requires login)(UNTESTED).

        Parameters:
            :tags:
                A space delimited list of tags.

            :file_:
                The file data encoded as a multipart form.

            :rating:
                The rating for the post. Can be: safe, questionable, or
                explicit.

            :source:
                If this is a URL, Danbooru will download the file.

            :is_rating_locked:
                Set to true to prevent others from changing the rating.

            :is_note_locked:
                Set to true to prevent others from adding notes.

            :parent_id:
                The ID of the parent post.

            :md5:
                Supply an MD5 if you want Danbooru to verify the file after
                uploading. If the MD5 doesn't match, the post is destroyed.
        """

        params = {'post[tags]': tags}

        if source is not None or file_ is not None:
            if file_ is not None:
                params['post[file]'] = file_
            if source is not None:
                params['post[source]'] = source
            if rating is not None:
                params['post[rating]'] = rating
            if is_rating_locked is not None:
                params['post[is_rating_locked]'] = is_rating_locked
            if is_note_locked is not None:
                params['post[is_note_locked]'] = is_note_locked
            if parent_id is not None:
                params['post[parent_id]'] = parent_id
            if md5 is not None:
                params['md5'] = md5

            return self._json_load('posts_create', params)
        else:
            raise PybooruError('source of file_ is required')

    def posts_update(self, id_, tags, file_, rating, source, is_rating_locked,
                     is_note_locked, parent_id):
        """This function update a specific post. Only the id_ parameter is
        required. Leave the other parameters blank if you don't want to
        change them (Requires login)(UNESTED).

        Parameters:
            :id_:
                The id number of the post to update (Type: INT).

            :tags:
                A space delimited list of tags (Type: STR).

            :file_:
                The file data ENCODED as a multipart form.

            :rating:
                The rating for the post. Can be: safe, questionable, or
                explicit.

            :source:
                If this is a URL, Danbooru will download the file.

            :is_rating_locked:
                Set to true to prevent others from changing the rating.

            :is_note_locked:
                Set to true to prevent others from adding notes.

            :parent_id:
                The ID of the parent post.
        """

        params = {'id': id_}

        if tags is not None:
            params['post[tags]'] = tags
        if file_ is not None:
            params['post[file]'] = file_
        if rating is not None:
            params['post[rating]'] = rating
        if source is not None:
            params['post[source]'] = source
        if is_rating_locked is not None:
            params['post[is_rating_locked]'] = is_rating_locked
        if is_note_locked is not None:
            params['post[is_note_locked]'] = is_note_locked
        if parent_id is not None:
            params['post[parent_id]'] = parent_id

        return self._json_load('posts_update', params)

    def posts_destroy(self, id_):
        """This function destroy a specific post. You must also be the user
        who uploaded the post (or you must be a moderator).
        (Requires Login)(UNTESTED).

        Parameters:
            :id_:
                The id number of the post to delete.
        """

        params = {'id': id_}
        response = self._json_load('posts_destroy', params)
        return response['success']

    def posts_revert_tags(self, id_, history_id):
        """This action reverts a post to a previous set of tags
        (Requires login)(UNTESTED).

        Parameters:
            :id_:
                The post id number to update (Type: INT).

            :history_id:
                The id number of the tag history.
        """

        params = {'id': id_, 'history_id': history_id}
        return self._json_load('posts_revert_tags', params)

    def posts_vote(self, id_, score):
        """This action lets you vote for a post (Requires login).

        Parameters:
            :id_:
                The post id (Type: INT).

            :score:
                Be can:
                    0: No voted or Remove vote.
                    1: Good.
                    2: Great.
                    3: Favorite, add post to favorites.
        """

        if score <= 3:
            params = {'id': id_, 'score': score}
            return self._json_load('posts_vote', params)
        else:
            raise PybooruError('Value of score only can be 0, 1, 2 and 3.')

    def tags_list(self, name=None, id_=None, limit=0, page=1, order='name',
                  after_id=None):
        """Get a list of tags.

        Parameters:
            :name:
                The exact name of the tag.

            :id_:
                The id number of the tag.

            :limit:
                How many tags to retrieve. Setting this to 0 will return
                every tag (Default value: 0).

            :page:
                The page number.

            :order:
                Can be 'date', 'name' or 'count' (Default: name).

            :after_id:
                Return all tags that have an id number greater than this.
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
        """This action lets you update tag (Requires login)(UNTESTED).

        Parameters:
            :name:
                The name of the tag to update.

            :tag_type:
                The tag type.
                    General: 0.
                    artist: 1.
                    copyright: 3.
                    character: 4.

            :is_ambiguous:
                Whether or not this tag is ambiguous. Use 1 for true and 0
                for false.
        """

        params = {'name': name, 'tag[tag_type]': tag_type,
                  'tag[is_ambiguous]': is_ambiguous}

        return self._json_load('tags_update', params)

    def tags_related(self, tags, type_=None):
        """Get a list of related tags.

        Parameters:
            :tags:
                The tag names to query.

            :type_:
                Restrict results to this tag type. Can be general, artist,
                copyright, or character (Default value: None).
        """

        params = {'tags': tags}

        if type_ is not None:
            params['type'] = type_

        return self._json_load('tags_related', params)

    def artists_list(self, name=None, order=None, page=1):
        """Get a list of artists.

        Parameters:
            :name:
                The name (or a fragment of the name) of the artist.

            :order:
                Can be date or name (Default value: None).

            :page:
                The page number.
        """

        params = {'page': page}

        if name is not None:
            params['name'] = name
        if order is not None:
            params['order'] = order

        return self._json_load('artists_list', params)

    def artists_create(self, name, urls, alias, group):
        """This function create a artist (Requires login)(UNTESTED).

        Parameters:
            :name:
                The artist's name.

            :urls:
                A list of URLs associated with the artist, whitespace delimited.

            :alias:
                The artist that this artist is an alias for. Simply enter the
                alias artist's name.

            :group:
                The group or cicle that this artist is a member of. Simply
                enter the group's name.
        """

        params = {'artist[name]': name, 'artist[urls]': urls,
                  'artist[alias]': alias, 'artist[group]': group}
        return self._json_load('artists_create', params)

    def artists_update(self, id_, name=None, urls=None, alias=None, group=None):
        """This function update an artists. Only the id_ parameter is required.
        The other parameters are optional. (Requires login)(UNTESTED).

        Parameters:
            :id_:
                The id of thr artist to update (Type: INT).

            :name:
                The artist's name.

            :urls:
                A list of URLs associated with the artist, whitespace delimited.

            :alias:
                The artist that this artist is an alias for. Simply enter the
                alias artist's name.

            :group:
                The group or cicle that this artist is a member of. Simply
                enter the group's name.
        """

        params = {'id': id_}

        if name is not None:
            params['artist[name]'] = name
        if urls is not None:
            params['artist[urls]'] = urls
        if alias is not None:
            params['artist[alias]'] = alias
        if group is not None:
            params['artist[group]'] = group

        return self._json_load('artists_update', params)

    def artists_destroy(self, id_):
        """This action lets you remove artist (Requires login)(UNTESTED).

        Parameters:
            :id_:
                The id of the artist to destroy (Type: INT).
        """

        params = {'id': id_}
        response = self._json_load('artists_destroy', params)
        return response['success']

    def comments_show(self, id_):
        """Get a specific comment.

        Parameters:
            :id_:
                The id number of the comment to retrieve (Type: INT).
        """

        params = {'id': id_}
        return self._json_load('comments_show', params)

    def comments_create(self, post_id, comment_body):
        """This action lets you create a comment (Requires login).

        Parameters:
            :post_id:
                The post id number to which you are responding (Type: INT).

            :comment_body:
                The body of the comment.
        """

        params = {'comment[post_id]': post_id,
                  'comment[body]': comment_body}
        response = self._json_load('comments_create', params)
        return response['success']

    def comments_destroy(self, id_=None):
        """Remove a specific comment (Requires login).

        Parameters:
            :id_:
                The id number of the comment to remove (Type: INT).
        """

        params = {'id': id_}
        response = self._json_load('comments_destroy', params)
        return response['success']

    def wiki_list(self, query=None, order='title', limit=100, page=1):
        """This function retrieves a list of every wiki page.

        Parameters:
            :query:
                A word or phrase to search for (Default: None).

            :order:
                Can be: title, date (Default: title).

            :limit:
                The number of pages to retrieve (Default: 100).

            :page:
                The page number.
        """

        params = {'order': order, 'limit': limit, 'page': page}

        if query is not None:
            params['query'] = query

        return self._json_load('wiki_list', params)

    def wiki_create(self, title, body):
        """This action lets you create a wiki page (Requires login)(UNTESTED).

        Parameters:
            :title:
                The title of the wiki page.

            :body:
                The body of the wiki page.
        """

        params = {'wiki_page[title]': str(title), 'wiki_page[body]': str(body)}
        return self._json_load('wiki_create', params)

    def wiki_update(self, page_title, new_title, page_body):
        """This action lets you update a wiki page (Requires login)(UNTESTED).

        Parameters:
            :page_title:
                The title of the wiki page to update.

            :new_title:
                The new title of the wiki page.

            :page_body:
                The new body of the wiki page.
        """

        params = {'title': page_title, 'wiki_page[title]': new_title,
                  'wiki_page[body]': page_body}
        return self._json_load('wiki_update', params)

    def wiki_show(self, title, version=None):
        """Get a specific wiki page.

        Parameters:
            :title:
                The title of the wiki page to retrieve.

            :version:
                The version of the page to retrieve.
        """

        params = {'title': title}

        if version is not None:
            params['version'] = version

        return self._json_load('wiki_show', params)

    def wiki_destroy(self, title):
        """This function delete a specific wiki page (Requires login)(UNTESTED)
        (Only moderators).

        Params:
            :title:
                The title of the page to delete.
        """

        params = {'title': title}
        response = self._json_load('wiki_destroy', params)
        return response['success']

    def wiki_lock(self, title):
        """This function lock a specific wiki page (Requires login)(UNTESTED)
        (Only moderators).

        Params:
            :title:
                The title of the page to lock.
        """

        params = {'title': title}
        response = self._json_load('wiki_lock', params)
        return response['success']

    def wiki_unlock(self, title):
        """This function unlock a specific wiki page (Requires login)(UNTESTED)
        (Only moderators).

        Params:
            :title:
                The title of the page to unlock.
        """

        params = {'title': title}
        response = self._json_load('wiki_unlock', params)
        return response['success']

    def wiki_revert(self, title, version):
        """This function revert a specific wiki page (Requires login)(UNTESTED).

        Parameters:
            :title:
                The title of the wiki page to update.

            :version:
                The version to revert to.
        """

        params = {'title': title, 'version': version}
        response = self._json_load('wiki_revert', params)
        return response['success']

    def wiki_history(self, title):
        """Get history of specific wiki page.

        Parameters:
            :title:
                The title of the wiki page to retrieve versions for.
        """

        params = {'title': title}
        return self._json_load('wiki_history', params)

    def notes_list(self, post_id=None):
        """Get note list

        Parameters:
            :post_id:
                The post id number to retrieve notes for (Default: None)
                (Type: INT).
        """

        if post_id is not None:
            params = {'post_id': post_id}
            return self._json_load('notes_list', params)
        else:
            return self._json_load('notes_list')

    def notes_search(self, query):
        """Search specific note.

        Parameters:
            :query:
                A word or phrase to search for.
        """

        params = {'query': query}
        return self._json_load('notes_search', params)

    def notes_history(self, post_id=None, id_=None, limit=10, page=1):
        """Get history of notes.

        Parameters:
            :post_id:
                The post id number to retrieve note versions for.

            :id_:
                The note id number to retrieve versions for (Type: INT).

            :limit:
                How many versions to retrieve (Default: 10).

            :page:
                The note id number to retrieve versions for.
        """

        params = {'limit': limit, 'page': page}

        if post_id is not None:
            params['post_id'] = post_id
        elif id_ is not None:
            params['id'] = id_

        return self._json_load('notes_history', params)

    def notes_revert(self, id_, version):
        """This function revert a specific note (Requires login)(UNTESTED).

        Parameters:
            :id_:
                The note id to update (Type: INT).

            :version:
                The version to revert to.
        """

        params = {'id': id_, 'version': version}
        response = self._json_load('wiki_revert', params)
        return response['success']

    def notes_create_update(self, post_id, x, y, width, height,
                            is_active, body, id_=None):
        """This function create or update note (Requires login)(UNTESTED).

        Parameters:
            :post_id:
                The post id number this note belongs to.

            :x:
                The x coordinate of the note.

            :y:
                The y coordinate of the note.

            :width:
                The width of the note.

            :height:
                The height of the note.

            :is_active:
                Whether or not the note is visible. Set to 1 for active, 0 for
                inactive.

            :body:
                The note message.

            :id_:
                If you are updating a note, this is the note id number to
                update.
        """

        params = {'note[post_id]': post_id, 'note[x]': x, 'note[y]': y,
                  'note[width]': width, 'note[height]': height,
                  'note[body]': body}

        if id_ is not None:
            params['id'] = id_
        if is_active <= 1:
            params['note[is_active]'] = is_active
        else:
            raise PybooruError('is_active parameters required 1 or 0')

        return self._json_load('notes_create_update', params)

    def users_search(self, name=None, id_=None):
        """Search users. If you don't specify any parameters you'll
        get a listing of all users.

        Parameters:
            :name:
                The name of the user.

            :id_:
                The id number of the user.
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
            :parent_id:
                The parent ID number. You'll return all the responses to that
                forum post.
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
            :query:
                The title.

            :page:
                The page.
        """

        params = {'page': page}

        if query is not None:
            params['query': query]

        return self._json_load('pools_list', params)

    def pools_posts(self, id_=None, page=1):
        """Get pools posts. If you don't specify any parameters you'll get a
        list of all pools.

        Parameters:
            :id_:
                The pool id number.

            :page:
                The page.
        """

        params = {'page': page}

        if id_ is not None:
            params['id'] = id_

        return self._json_load('pools_posts', params)

    def pools_update(self, id_, name, is_public, description):
        """This function update a pool (Requires login)(UNTESTED).

        Parameters:
            :id_:
                The pool id number.

            :name:
                The name.

            :is_public:
                1 or 0, whether or not the pool is public.

            :description:
                A description of the pool.
        """

        params = {'id': id_, 'pool[name]': name,
                  'pool[description]': description}

        if is_public <= 1:
            params['pool[is_public]'] = is_public
        else:
            raise PybooruError('is_public require 1 or 0')

        return self._json_load('pools_update', params)

    def pools_create(self, name, is_public, description):
        """This function create a pool (Require login)(UNTESTED).

        Parameters:
            :name:
                The name.

            :is_public:
                1 or 0, whether or not the pool is public.

            :description:
                A description of the pool.
        """

        params = {'pool[name]': name, 'pool[description]': description}

        if is_public <= 1:
            params['pool[name]'] = is_public
        else:
            raise PybooruError('is_public required 1 or 0')

        return self._json_load('pools_create', params)

    def pools_destroy(self, id_):
        """This function destroy a specific pool (Require login)(UNTESTED).

        Parameters:
            :id_:
                The pool id number (Type: INT).
        """

        params = {'id': id_}
        response = self._json_load('pools_destroy', params)
        return response['success']

    def pools_add_post(self, pool_id, post_id):
        """This function add a post (Require login)(UNTESTED).

        Parameters:
            :pool_id:
                The pool to add the post to.

            :post_id:
                The post to add.
        """

        params = {'pool_id': pool_id, 'post_id': post_id}
        return self._json_load('pools_add_post', params)

    def pools_remove_post(self, pool_id, post_id):
        """This function remove a post (Require login)(UNTESTED).

        Parameters:
            :pool_id:
                The pool to remove the post to.

            :post_id:
                The post to remove.
        """

        params = {'pool_id': pool_id, 'post_id': post_id}
        return self._json_load('pools_remove_post', params)

    def favorites_list_users(self, id_):
        """Return a list with all users who have added to favorites a specific
        post.

        Parameters:
            :id_:
                The post id (Type: INT).
        """

        params = {'id': id_}
        response = self._json_load('favorites_list_users', params)
        # Return list with users
        return response['favorited_users'].split(',')
