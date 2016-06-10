# -*- coding: utf-8 -*-

"""pybooru.api

This module contains all API calls of Danbooru/Moebooru for Pybooru.

Classes:
    ApiFunctionsMixin -- Contains all API calls.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .exceptions import PybooruError


class ApiFunctionsMixin(object):
    """Contains all Danbooru/Moebooru API calls.

    API Version: 1.13.0+update.3
    doc: http://konachan.com/help/api or https://yande.re/help/api
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            tags: The tags to search for. Any tag combination that works on the
                  web site will work here. This includes all the meta-tags.
            limit: How many posts you want to retrieve. There is a limit of 100
                   posts per request.
            page: The page number.
        """
        return self._request('post', params)

    def post_create(self, tags, file_=None, rating=None, source=None,
                    rating_locked=None, note_locked=None, parent_id=None,
                    md5=None):
        """Function to create a new post.

        There are only two mandatory fields: you need to supply the
        'post[tags]', and you need to supply the 'post[file]', either through a
        multipart form or through a source URL (Requires login) (UNTESTED).

        Parameters:
            tags: A space delimited list of tags.
            file_: The file data encoded as a multipart form. Path of content.
            rating: The rating for the post. Can be: safe, questionable,
                    or explicit.
            source: If this is a URL, Danbooru/Moebooru will download the
                    file.
            rating_locked: Set to true to prevent others from changing
                           the rating.
            note_locked: Set to true to prevent others from adding
                         notes.
            parent_id: The ID of the parent post.
            md5: Supply an MD5 if you want Danbooru/Moebooru to verify the file
                 after uploading. If the MD5 doesn't match, the post is
                 destroyed.
        """
        params = {'post[tags]': tags}
        if file_ or source is not None:
            if file_ is not None:
                file_ = {'post[file]': open(file_, 'rb')}
            if source is not None:
                params['post[source]'] = source
            if rating is not None:
                params['post[rating]'] = rating
            if rating_locked is not None:
                params['post[is_rating_locked]'] = rating_locked
            if note_locked is not None:
                params['post[is_note_locked]'] = note_locked
            if parent_id is not None:
                params['post[parent_id]'] = parent_id
            if md5 is not None:
                params['md5'] = md5
            return self._request('post/create', params, 'POST', file_)
        else:
            raise PybooruError("'file_' or 'source' is required.")

    def post_update(self, id_, tags=None, file_=None, rating=None,
                    source=None, is_rating_locked=None, is_note_locked=None,
                    parent_id=None):
        """Function update a specific post.

        Only the 'id_' parameter is required. Leave the other parameters blank
        if you don't want to change them (Requires login).

        Parameters:
            id_: The id number of the post to update.
            tags: A space delimited list of tags. Specify previous tags.
            file_: The file data ENCODED as a multipart form.
            rating: The rating for the post. Can be: safe, questionable, or
                    explicit.
            source: If this is a URL, Danbooru/Moebooru will download the file.
            rating_locked: Set to true to prevent others from changing the
                           rating.
            note_locked: Set to true to prevent others from adding notes.
            parent_id: The ID of the parent post.
        """
        params = {'id': id_}
        if tags is not None:
            params['post[tags]'] = tags
        if file_ is not None:
            file_ = {'post[file]': open(file_, 'rb')}
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
        return self._request('post/update', params, 'POST')

    def post_destroy(self, id_):
        """Function to destroy a specific post.

        You must also be the user who uploaded the post (or you must be a
        moderator) (Requires Login) (UNTESTED).

        Parameters:
            id_: The id number of the post to delete.
        """
        return self._request('post/destroy', {'id': id_}, 'POST')

    def post_revert_tags(self, id_, history_id):
        """Function to reverts a post to a previous set of tags
        (Requires login) (UNTESTED).

        Parameters:
            id_: The post id number to update.
            history_id: The id number of the tag history.
        """
        params = {'id': id_, 'history_id': history_id}
        return self._request('post/revert_tags', params, 'POST')

    def post_vote(self, id_, score):
        """Action lets you vote for a post (Requires login).

        Parameters:
            id_: The post id.
            score:
                0: No voted or Remove vote.
                1: Good.
                2: Great.
                3: Favorite, add post to favorites.
        """
        if score <= 3:
            params = {'id': id_, 'score': score}
            return self._request('post/vote', params, 'POST')
        else:
            raise PybooruError("Value of 'score' only can be 0, 1, 2 or 3.")

    def tag_list(self, **params):
        """Get a list of tags.

        Parameters:
            name: The exact name of the tag.
            id: The id number of the tag.
            limit: How many tags to retrieve. Setting this to 0 will return
                   every tag (Default value: 0).
            page: The page number.
            order: Can be 'date', 'name' or 'count'.
            after_id: Return all tags that have an id number greater than this.
        """
        return self._request('tag', params)

    def tag_update(self, name=None, tag_type=None, is_ambiguous=None):
        """Action to lets you update tag (Requires login) (UNTESTED).

        Parameters:
            name: The name of the tag to update.
            tag_type:
                General: 0.
                artist: 1.
                copyright: 3.
                character: 4.
            is_ambiguous: Whether or not this tag is ambiguous. Use 1 for true
                          and 0 for false.
        """
        params = {'name': name}
        if tag_type is not None:
            params['tag[tag_type]'] = tag_type
        if is_ambiguous is not None:
            params['tag[is_ambiguous]'] = is_ambiguous
        return self._request('tag/update', params, 'POST')

    def tag_related(self, **params):
        """Get a list of related tags.

        Parameters:
            tags: The tag names to query.
            type: Restrict results to this tag type. Can be general, artist,
                  copyright, or character.
        """
        return self._request('tag/related', params)

    def artist_list(self, **params):
        """Get a list of artists.

        Parameters:
            name: The name (or a fragment of the name) of the artist.
            order: Can be date or name.
            page: The page number.
        """
        return self._request('artist', params)

    def artist_create(self, name, urls=None, alias=None, group=None):
        """Function to create a artist (Requires login) (UNTESTED).

        Parameters:
            name: The artist's name.
            urls: A list of URLs associated with the artist, whitespace
                  delimited.
            alias: The artist that this artist is an alias for. Simply enter
                   the alias artist's name.
            group: The group or cicle that this artist is a member of. Simply
                   enter the group's name.
        """
        params = {'artist[name]': name}
        if urls is not None:
            params['artist[urls]'] = urls
        if alias is not None:
            params['artist[alias]'] = alias
        if group is not None:
            params['artist[group]'] = group
        return self._request('artist/create', params, 'POST')

    def artist_update(self, id_, name=None, urls=None, alias=None, group=None):
        """Function to update an artists.

        Only the id_ parameter is required. The other parameters are optional.
        (Requires login) (UNTESTED).

        Parameters:
            id_: The id of thr artist to update (Type: INT).
            name: The artist's name.
            urls: A list of URLs associated with the artist, whitespace
                  delimited.
            alias: The artist that this artist is an alias for. Simply enter the
                   alias artist's name.
            group: The group or cicle that this artist is a member of. Simply
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
        return self._request('artist/update', params, 'POST')

    def artist_destroy(self, id_):
        """Action to lets you remove artist (Requires login) (UNTESTED).

        Parameters:
            id_: The id of the artist to destroy.
        """
        return self._request('artist/destroy', {'id': id_}, 'POST')

    def comment_show(self, id_):
        """Get a specific comment.

        Parameters:
            id_: The id number of the comment to retrieve.
        """
        return self._request('comment/show', {'id': id_})

    def comment_create(self, post_id, comment_body, anonymous=None):
        """Action to lets you create a comment (Requires login).

        Parameters:
            post_id: The post id number to which you are responding.
            comment_body: The body of the comment.
            anonymous: Set to 1 if you want to post this comment anonymously.
        """
        params = {}
        if post_id and comment_body is not None:
            params['comment[post_id]'] = post_id
            params['comment[body]'] = comment_body
            if anonymous is not None:
                params['comment[anonymous]'] = anonymous
            return self._request('comment/create', params, 'POST')
        else:
            raise PybooruError("Required 'post_id' and 'comment_body' "
                               "parameters")

    def comment_destroy(self, id_=None):
        """Remove a specific comment (Requires login).

        Parameters:
            id_: The id number of the comment to remove.
        """
        return self._request('comment/destroy', {'id': id_}, 'POST')

    def wiki_list(self, **params):
        """Function to retrieves a list of every wiki page.

        Parameters:
            query: A word or phrase to search for (Default: None).
            order: Can be: title, date (Default: title).
            limit: The number of pages to retrieve (Default: 100).
            page: The page number.
        """
        return self._request('wiki', params)

    def wiki_create(self, title, body):
        """Action to lets you create a wiki page (Requires login) (UNTESTED).

        Parameters:
            title: The title of the wiki page.
            body: The body of the wiki page.
        """
        params = {'wiki_page[title]': title, 'wiki_page[body]': body}
        return self._request('wiki/create', params, 'POST')

    def wiki_update(self, page_title, new_title=None, page_body=None):
        """Action to lets you update a wiki page (Requires login) (UNTESTED).

        Parameters:
            page_title: The title of the wiki page to update.
            new_title: The new title of the wiki page.
            page_body: The new body of the wiki page.
        """
        params = {'title': page_title}
        if new_title is not None:
            params['wiki_page[title]'] = new_title
        if page_body is not None:
            params['wiki_page[body]'] = page_body
        return self._request('wiki/update', params, 'POST')

    def wiki_show(self, **params):
        """Get a specific wiki page.

        Parameters:
            title: The title of the wiki page to retrieve.
            version: The version of the page to retrieve.
        """
        return self._request('wiki/show', params)

    def wiki_destroy(self, title):
        """Function to delete a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            title: The title of the page to delete.
        """
        return self._request('wiki/destroy', {'title': title}, 'POST')

    def wiki_lock(self, title):
        """Function to lock a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            title: The title of the page to lock.
        """
        return self._request('wiki/lock', {'title': title}, 'POST')

    def wiki_unlock(self, title):
        """Function to unlock a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            title: The title of the page to unlock.
        """
        return self._request('wiki/unlock', {'title': title}, 'POST')

    def wiki_revert(self, title, version):
        """Function to revert a specific wiki page (Requires login) (UNTESTED).

        Parameters:
            title: The title of the wiki page to update.
            version: The version to revert to.
        """
        params = {'title': title, 'version': version}
        return self._request('wiki/revert', params, 'POST')

    def wiki_history(self, title):
        """Get history of specific wiki page.

        Parameters:
            title: The title of the wiki page to retrieve versions for.
        """
        return self._request('wiki/history', {'title': title})

    def note_list(self, **params):
        """Get note list.

        Parameters:
            post_id: The post id number to retrieve notes for.
        """
        return self._request('note', params)

    def note_search(self, query):
        """Search specific note.

        Parameters:
            query: A word or phrase to search for.
        """
        return self._request('note/search', {'query': query})

    def notes_history(self, **params):
        """Get history of notes.

        Parameters:
            post_id: The post id number to retrieve note versions for.
            id_: The note id number to retrieve versions for.
            limit: How many versions to retrieve (Default: 10).
            page: The note id number to retrieve versions for.
        """
        return self._request('note/history', params)

    def note_revert(self, id_, version):
        """Function to revert a specific note (Requires login) (UNTESTED).

        Parameters:
            id: The note id to update.
            version: The version to revert to.
        """
        params = {'id': id_, 'version': version}
        return self._request('note/revert', params, 'POST')

    def note_create_update(self, post_id=None, coor_x=None, coor_y=None,
                           width=None, height=None, is_active=None, body=None,
                           id_=None):
        """Function to create or update note (Requires login) (UNTESTED).

        Parameters:
            post_id: The post id number this note belongs to.
            coor_x: The X coordinate of the note.
            coor_y: The Y coordinate of the note.
            width: The width of the note.
            height: The height of the note.
            is_active: Whether or not the note is visible. Set to 1 for
                       active, 0 for inactive.
            body: The note message.
            id_: If you are updating a note, this is the note id number to
                 update.
        """
        params = {}
        if id_ is not None:
            params['id'] = id_
        if post_id is not None:
            params['note[post]'] = post_id
        if coor_x is not None:
            params['note[x]'] = coor_x
        if coor_y is not None:
            params['note[y]'] = coor_y
        if width is not None:
            params['note[width]'] = width
        if height is not None:
            params['note[height]'] = height
        if body is not None:
            params['note[body]'] = body
        if is_active is not None:
            params['note[is_active]'] = is_active
        return self._request('note/update', params, 'POST')

    def user_search(self, **params):
        """Search users.

        If you don't specify any parameters you'll get a listing of all users.

        Parameters:
            id: The id number of the user.
            name: The name of the user.
        """
        return self._request('user', params)

    def forum_list(self, **params):
        """Function to get forum posts.

        If you don't specify any parameters you'll get a listing of all users.

        Parameters:
            parent_id: The parent ID number. You'll return all the responses
                       to that forum post.
        """
        return self._request('forum', params)

    def pool_list(self, **params):
        """Function to get pools.

        If you don't specify any parameters you'll get a list of all pools.

        Parameters:
            query: The title.
            page: The page.
        """
        return self._request('pool', params)

    def pool_posts(self, **params):
        """Function to get pools posts.

        If you don't specify any parameters you'll get a list of all pools.

        Parameters:
            id: The pool id number.
            page: The page.
        """
        return self._request('pool/show', params)

    def pool_update(self, id_, name=None, is_public=None,
                    description=None):
        """Function to update a pool (Requires login) (UNTESTED).

        Parameters:
            id_: The pool id number.
            name: The name.
            is_public: 1 or 0, whether or not the pool is public.
            description: A description of the pool.
        """
        params = {'id': id_}
        if name is not None:
            params['pool[name]'] = name
        if is_public is not None:
            params['pool[is_public]'] = is_public
        if name is not None:
            params['pool[name]'] = name
        if description is not None:
            params['pool[description]'] = description
        return self._request('pool/update', params, 'POST')

    def pool_create(self, name, description, is_public):
        """Function to create a pool (Require login) (UNTESTED).

        Parameters:
            name: The name.
            description: A description of the pool.
            is_public: 1 or 0, whether or not the pool is public.
        """
        params = {'pool[name]': name, 'pool[description]': description,
                  'pool[name]': is_public}
        return self._request('pool/create', params, 'POST')

    def pool_destroy(self, id_):
        """Function to destroy a specific pool (Require login) (UNTESTED).

        Parameters:
            id_: The pool id number.
        """
        return self._request('pool/destroy', {'id': id_}, 'POST')

    def pool_add_post(self, **params):
        """Function to add a post (Require login) (UNTESTED).

        Parameters:
            pool_id: The pool to add the post to.
            post_id: The post to add.
        """
        return self._request('pool/add_post', params, 'POST')

    def pool_remove_post(self, **params):
        """Function to remove a post (Require login) (UNTESTED).

        Parameters:
            pool_id: The pool to remove the post to.
            post_id: The post to remove.
        """
        return self._request('pool/remove_post', params, 'POST')

    def favorites_list_users(self, id_):
        """Function to return a list with all users who have added to favorites
        a specific post.

        Parameters:
            id_: The post id.
        """
        response = self._request('favorite/list_users', {'id': id_})
        # Return list with users
        return response['favorited_users'].split(',')
