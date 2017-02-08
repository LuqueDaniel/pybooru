# -*- coding: utf-8 -*-

"""pybooru.api_moebooru

This module contains all API calls of Moebooru.

Classes:
    MoebooruApi_Mixin -- Contains all API calls.
"""

# __future__ imports
from __future__ import absolute_import

# pybooru imports
from .exceptions import PybooruAPIError


class MoebooruApi_Mixin(object):
    """Contains all Moebooru API calls.

    * API Versions: 1.13.0+update.3 and 1.13.0
    * doc: https://yande.re/help/api or http://konachan.com/help/api
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            tags (str): The tags to search for. Any tag combination that works
                        on the web site will work here. This includes all the
                        meta-tags.
            limit (int): How many posts you want to retrieve. There is a limit
                         of 100:param  posts per request.
            page (int): The page number.
        """
        return self._get('post', params)

    def post_create(self, tags, file_=None, rating=None, source=None,
                    rating_locked=None, note_locked=None, parent_id=None,
                    md5=None):
        """Function to create a new post (Requires login).

        There are only two mandatory fields: you need to supply the
        'tags', and you need to supply the 'file_', either through a
        multipart form or through a source URL (Requires login) (UNTESTED).

        Parameters:
            tags (str): A space delimited list of tags.
            file_ (str): The file data encoded as a multipart form. Path of
                         content.
            rating (str): The rating for the post. Can be: safe, questionable,
                          or explicit.
            source (str): If this is a URL, Moebooru will download the file.
            rating_locked (bool): Set to True to prevent others from changing
                                  the rating.
            note_locked (bool): Set to True to prevent others from adding notes.
            parent_id (int): The ID of the parent post.
            md5 (str): Supply an MD5 if you want Moebooru to verify the file
                       after uploading. If the MD5 doesn't match, the post is
                       destroyed.

        Raises:
            PybooruAPIError: When file or source are empty.
        """
        if file_ or source is not None:
            params = {
                'post[tags]': tags,
                'post[source]': source,
                'post[rating]': rating,
                'post[is_rating_locked]': rating_locked,
                'post[is_note_locked]': note_locked,
                'post[parent_id]': parent_id,
                'md5': md5}
            file_ = {'post[file]': open(file_, 'rb')}
            return self._get('post/create', params, 'POST', file_)
        else:
            raise PybooruAPIError("'file_' or 'source' is required.")

    def post_update(self, post_id, tags=None, file_=None, rating=None,
                    source=None, is_rating_locked=None, is_note_locked=None,
                    parent_id=None):
        """Update a specific post.

        Only the 'post_id' parameter is required. Leave the other parameters
        blank if you don't want to change them (Requires login).

        Parameters:
            post_id (int): The id number of the post to update.
            tags (str): A space delimited list of tags. Specify previous tags.
            file_ (str): The file data ENCODED as a multipart form.
            rating (str): The rating for the post. Can be: safe, questionable,
                          or explicit.
            source (str): If this is a URL, Moebooru will download the file.
            rating_locked (bool): Set to True to prevent others from changing
                                  the rating.
            note_locked (bool): Set to True to prevent others from adding
                                notes.
            parent_id (int): The ID of the parent post.
        """
        params = {
            'id': post_id,
            'post[tags]': tags,
            'post[rating]': rating,
            'post[source]': source,
            'post[is_rating_locked]': is_rating_locked,
            'post[is_note_locked]': is_note_locked,
            'post[parent_id]': parent_id
            }
        if file_ is not None:
            file_ = {'post[file]': open(file_, 'rb')}
            return self._get('post/update', params, 'PUT', file_)
        else:
            return self._get('post/update', params, 'PUT')

    def post_destroy(self, post_id):
        """Function to destroy a specific post.

        You must also be the user who uploaded the post (or you must be a
        moderator) (Requires Login) (UNTESTED).

        Parameters:
            post_id (int): The id number of the post to delete.
        """
        return self._get('post/destroy', {'id': post_id}, method='DELETE')

    def post_revert_tags(self, post_id, history_id):
        """Function to reverts a post to a previous set of tags
        (Requires login) (UNTESTED).

        Parameters:
            post_id (int): The post id number to update.
            history_id (int): The id number of the tag history.
        """
        params = {'id': post_id, 'history_id': history_id}
        return self._get('post/revert_tags', params, 'PUT')

    def post_vote(self, post_id, score):
        """Action lets you vote for a post (Requires login).

        Parameters:
            post_id (int): The post id.
            score (int):
                * 0: No voted or Remove vote.
                * 1: Good.
                * 2: Great.
                * 3: Favorite, add post to favorites.

        Raises:
            PybooruAPIError: When score is > 3.
        """
        if score <= 3 and score >= 0:
            params = {'id': post_id, 'score': score}
            return self._get('post/vote', params, 'POST')
        else:
            raise PybooruAPIError("Value of 'score' only can be 0, 1, 2 or 3.")

    def tag_list(self, **params):
        """Get a list of tags.

        Parameters:
            name (str): The exact name of the tag.
            id (int): The id number of the tag.
            limit (int): How many tags to retrieve. Setting this to 0 will
                         return every tag (Default value: 0).
            page (int): The page number.
            order (str): Can be 'date', 'name' or 'count'.
            after_id (int): Return all tags that have an id number greater
                            than this.
        """
        return self._get('tag', params)

    def tag_update(self, name=None, tag_type=None, is_ambiguous=None):
        """Action to lets you update tag (Requires login) (UNTESTED).

        Parameters:
            name (str): The name of the tag to update.
            tag_type (int):
                * General: 0.
                * artist: 1.
                * copyright: 3.
                * character: 4.
            is_ambiguous (int): Whether or not this tag is ambiguous. Use 1
                                for True and 0 for False.
        """
        params = {
            'name': name,
            'tag[tag_type]': tag_type,
            'tag[is_ambiguous]': is_ambiguous
            }
        return self._get('tag/update', params, 'PUT')

    def tag_related(self, **params):
        """Get a list of related tags.

        Parameters:
            tags (str): The tag names to query.
            type (str): Restrict results to this tag type. Can be general,
                        artist, copyright, or character.
        """
        return self._get('tag/related', params)

    def artist_list(self, **params):
        """Get a list of artists.

        Parameters:
            name (str): The name (or a fragment of the name) of the artist.
            order (str): Can be date or name.
            page (int): The page number.
        """
        return self._get('artist', params)

    def artist_create(self, name, urls=None, alias=None, group=None):
        """Function to create an artist (Requires login) (UNTESTED).

        Parameters:
            name (str): The artist's name.
            urls (str): A list of URLs associated with the artist, whitespace
                        delimited.
            alias (str): The artist that this artist is an alias for. Simply
                         enter the alias artist's name.
            group (str): The group or cicle that this artist is a member of.
                         Simply:param  enter the group's name.
        """
        params = {
            'artist[name]': name,
            'artist[urls]': urls,
            'artist[alias]': alias,
            'artist[group]': group
            }
        return self._get('artist/create', params, method='POST')

    def artist_update(self, artist_id, name=None, urls=None, alias=None,
                      group=None):
        """Function to update artists (Requires Login) (UNTESTED).

        Only the artist_id parameter is required. The other parameters are
        optional.

        Parameters:
            artist_id (int): The id of thr artist to update (Type: INT).
            name (str): The artist's name.
            urls (str): A list of URLs associated with the artist, whitespace
                        delimited.
            alias (str): The artist that this artist is an alias for. Simply
                         enter the alias artist's name.
            group (str): The group or cicle that this artist is a member of.
                         Simply enter the group's name.
        """
        params = {
            'id': artist_id,
            'artist[name]': name,
            'artist[urls]': urls,
            'artist[alias]': alias,
            'artist[group]': group
            }
        return self._get('artist/update', params, method='PUT')

    def artist_destroy(self, artist_id):
        """Action to lets you remove artist (Requires login) (UNTESTED).

        Parameters:
            artist_id (int): The id of the artist to destroy.
        """
        return self._get('artist/destroy', {'id': artist_id}, method='POST')

    def comment_show(self, comment_id):
        """Get a specific comment.

        Parameters:
            comment_id (str): The id number of the comment to retrieve.
        """
        return self._get('comment/show', {'id': comment_id})

    def comment_create(self, post_id, comment_body, anonymous=None):
        """Action to lets you create a comment (Requires login).

        Parameters:
            post_id (int): The post id number to which you are responding.
            comment_body (str): The body of the comment.
            anonymous (int): Set to 1 if you want to post this comment
                             anonymously.
        """
        params = {
            'comment[post_id]': post_id,
            'comment[body]': comment_body,
            'comment[anonymous]': anonymous
            }
        return self._get('comment/create', params, method='POST')

    def comment_destroy(self, comment_id):
        """Remove a specific comment (Requires login).

        Parameters:
            comment_id (int): The id number of the comment to remove.
        """
        return self._get('comment/destroy', {'id': comment_id}, 'DELETE')

    def wiki_list(self, **params):
        """Function to retrieves a list of every wiki page.

        Parameters:
            query (str): A word or phrase to search for (Default: None).
            order (str): Can be: title, date (Default: title).
            limit (int): The number of pages to retrieve (Default: 100).
            page (int): The page number.
        """
        return self._get('wiki', params)

    def wiki_create(self, title, body):
        """Action to lets you create a wiki page (Requires login) (UNTESTED).

        Parameters:
            title (str): The title of the wiki page.
            body (str): The body of the wiki page.
        """
        params = {'wiki_page[title]': title, 'wiki_page[body]': body}
        return self._get('wiki/create', params, method='POST')

    def wiki_update(self, title, new_title=None, page_body=None):
        """Action to lets you update a wiki page (Requires login) (UNTESTED).

        Parameters:
            title (str): The title of the wiki page to update.
            new_title (str): The new title of the wiki page.
            page_body (str): The new body of the wiki page.
        """
        params = {
            'title': title,
            'wiki_page[title]': new_title,
            'wiki_page[body]': page_body
            }
        return self._get('wiki/update', params, method='PUT')

    def wiki_show(self, **params):
        """Get a specific wiki page.

        Parameters:
            title (str): The title of the wiki page to retrieve.
            version (int): The version of the page to retrieve.
        """
        return self._get('wiki/show', params)

    def wiki_destroy(self, title):
        """Function to delete a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            title (str): The title of the page to delete.
        """
        return self._get('wiki/destroy', {'title': title}, method='DELETE')

    def wiki_lock(self, title):
        """Function to lock a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            title (str): The title of the page to lock.
        """
        return self._get('wiki/lock', {'title': title}, 'POST')

    def wiki_unlock(self, title):
        """Function to unlock a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            title (str): The title of the page to unlock.
        """
        return self._get('wiki/unlock', {'title': title}, method='POST')

    def wiki_revert(self, title, version):
        """Function to revert a specific wiki page (Requires login) (UNTESTED).

        Parameters:
            title (str): The title of the wiki page to update.
            version (int): The version to revert to.
        """
        params = {'title': title, 'version': version}
        return self._get('wiki/revert', params, method='PUT')

    def wiki_history(self, title):
        """Get history of specific wiki page.

        Parameters:
            title (str): The title of the wiki page to retrieve versions for.
        """
        return self._get('wiki/history', {'title': title})

    def note_list(self, **params):
        """Get note list.

        Parameters:
            post_id (int): The post id number to retrieve notes for.
        """
        return self._get('note', params)

    def note_search(self, query):
        """Search specific note.

        Parameters:
            query (str): A word or phrase to search for.
        """
        return self._get('note/search', {'query': query})

    def note_history(self, **params):
        """Get history of notes.

        Parameters:
            post_id (int): The post id number to retrieve note versions for.
            id (int): The note id number to retrieve versions for.
            limit (int): How many versions to retrieve (Default: 10).
            page (int): The note id number to retrieve versions for.
        """
        return self._get('note/history', params)

    def note_revert(self, note_id, version):
        """Function to revert a specific note (Requires login) (UNTESTED).

        Parameters:
            note_id (int): The note id to update.
            version (int): The version to revert to.
        """
        params = {'id': note_id, 'version': version}
        return self._get('note/revert', params, method='PUT')

    def note_create_update(self, post_id=None, coor_x=None, coor_y=None,
                           width=None, height=None, is_active=None, body=None,
                           note_id=None):
        """Function to create or update note (Requires login) (UNTESTED).

        Parameters:
            post_id (int): The post id number this note belongs to.
            coor_x (int): The X coordinate of the note.
            coor_y (int): The Y coordinate of the note.
            width (int): The width of the note.
            height (int): The height of the note.
            is_active (int): Whether or not the note is visible. Set to 1 for
                             active, 0 for inactive.
            body (str): The note message.
            note_id (int): If you are updating a note, this is the note id
                           number to update.
        """
        params = {
            'id': note_id,
            'note[post]': post_id,
            'note[x]': coor_x,
            'note[y]': coor_y,
            'note[width]': width,
            'note[height]': height,
            'note[body]': body,
            'note[is_active]': is_active
            }
        return self._get('note/update', params, method='POST')

    def user_search(self, **params):
        """Search users.

        If you don't specify any parameters you'll _get a listing of all users.

        Parameters:
            id (int): The id number of the user.
            name (str): The name of the user.
        """
        return self._get('user', params)

    def forum_list(self, **params):
        """Function to get forum posts.

        If you don't specify any parameters you'll _get a listing of all users.

        Parameters:
            parent_id (int): The parent ID number. You'll return all the
                             responses to that forum post.
        """
        return self._get('forum', params)

    def pool_list(self, **params):
        """Function to get pools.

        If you don't specify any parameters you'll get a list of all pools.

        Parameters:
            query (str): The title.
            page (int): The page number.
        """
        return self._get('pool', params)

    def pool_posts(self, **params):
        """Function to get pools posts.

        If you don't specify any parameters you'll get a list of all pools.

        Parameters:
            id (int): The pool id number.
            page (int): The page number.
        """
        return self._get('pool/show', params)

    def pool_update(self, pool_id, name=None, is_public=None,
                    description=None):
        """Function to update a pool (Requires login) (UNTESTED).

        Parameters:
            pool_id (int): The pool id number.
            name (str): The name.
            is_public (int): 1 or 0, whether or not the pool is public.
            description (str): A description of the pool.
        """
        params = {
            'id': pool_id,
            'pool[name]': name,
            'pool[is_public]': is_public,
            'pool[description]': description
            }
        return self._get('pool/update', params, method='PUT')

    def pool_create(self, name, description, is_public):
        """Function to create a pool (Require login) (UNTESTED).

        Parameters:
            name (str): The name.
            description (str): A description of the pool.
            is_public (int): 1 or 0, whether or not the pool is public.
        """
        params = {'pool[name]': name, 'pool[description]': description,
                  'pool[is_public]': is_public}
        return self._get('pool/create', params, method='POST')

    def pool_destroy(self, pool_id):
        """Function to destroy a specific pool (Require login) (UNTESTED).

        Parameters:
            pool_id (int): The pool id number.
        """
        return self._get('pool/destroy', {'id': pool_id}, method='DELETE')

    def pool_add_post(self, **params):
        """Function to add a post (Require login) (UNTESTED).

        Parameters:
            pool_id (int): The pool to add the post to.
            post_id (int): The post to add.
        """
        return self._get('pool/add_post', params, method='PUT')

    def pool_remove_post(self, **params):
        """Function to remove a post (Require login) (UNTESTED).

        Parameters:
            pool_id (int): The pool to remove the post to.
            post_id (int): The post to remove.
        """
        return self._get('pool/remove_post', params, method='PUT')

    def favorite_list_users(self, post_id):
        """Function to return a list with all users who have added to favorites
        a specific post.

        Parameters:
            post_id (int): The post id.
        """
        response = self._get('favorite/list_users', {'id': post_id})
        # Return list with users
        return response['favorited_users'].split(',')
