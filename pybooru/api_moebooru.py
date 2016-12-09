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
            :param tags: The tags to search for. Any tag combination that works
                         on the web site will work here. This includes all the
                         meta-tags.
            :param limit: How many posts you want to retrieve. There is a limit
                          of 100:param  posts per request.
            :param page: The page number.
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
            :param tags: A space delimited list of tags.
            :param file_: The file data encoded as a multipart form. Path of
                          content.
            :param rating: The rating for the post. Can be: safe, questionable,
                           or explicit.
            :param source: If this is a URL, Moebooru will download the file.
            :param rating_locked: Set to true to prevent others from changing
                                  the rating.
            :param note_locked: Set to true to prevent others from adding
                                notes.
            :param parent_id: The ID of the parent post.
            :param md5: Supply an MD5 if you want Moebooru to verify the file
                        after uploading. If the MD5 doesn't match, the post is
                        destroyed.
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
            :param post_id: The id number of the post to update.
            :param tags: A space delimited list of tags. Specify previous tags.
            :param file_: The file data ENCODED as a multipart form.
            :param rating: The rating for the post. Can be: safe, questionable,
                           or explicit.
            :param source: If this is a URL, Moebooru will download the file.
            :param rating_locked: Set to true to prevent others from changing
                                  the rating.
            :param note_locked: Set to true to prevent others from adding
                                notes.
            :param parent_id: The ID of the parent post.
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
            :param Post_id: The id number of the post to delete.
        """
        return self._get('post/destroy', {'id': post_id}, 'DELETE')

    def post_revert_tags(self, post_id, history_id):
        """Function to reverts a post to a previous set of tags
        (Requires login) (UNTESTED).

        Parameters:
            :param post_id: The post id number to update.
            :param history_id: The id number of the tag history.
        """
        params = {'id': post_id, 'history_id': history_id}
        return self._get('post/revert_tags', params, 'PUT')

    def post_vote(self, post_id, score):
        """Action lets you vote for a post (Requires login).

        Parameters:
            :param post_id: The post id.
            :param score:
                * 0: No voted or Remove vote.
                * 1: Good.
                * 2: Great.
                * 3: Favorite, add post to favorites.
        """
        if score <= 3:
            params = {'id': post_id, 'score': score}
            return self._get('post/vote', params, 'POST')
        else:
            raise PybooruAPIError("Value of 'score' only can be 0, 1, 2 or 3.")

    def tag_list(self, **params):
        """Get a list of tags.

        Parameters:
            :param name: The exact name of the tag.
            :param id: The id number of the tag.
            :param limit: How many tags to retrieve. Setting this to 0 will
                          return every tag (Default value: 0).
            :param page: The page number.
            :param order: Can be 'date', 'name' or 'count'.
            :param after_id: Return all tags that have an id number greater
                             than this.
        """
        return self._get('tag', params)

    def tag_update(self, name=None, tag_type=None, is_ambiguous=None):
        """Action to lets you update tag (Requires login) (UNTESTED).

        Parameters:
            :param name: The name of the tag to update.
            :param tag_type:
                * General: 0.
                * artist: 1.
                * copyright: 3.
                * character: 4.
            :param is_ambiguous: Whether or not this tag is ambiguous. Use 1
                                 for true and 0 for false.
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
            :param tags: The tag names to query.
            :param type: Restrict results to this tag type. Can be general,
                         artist, copyright, or character.
        """
        return self._get('tag/related', params)

    def artist_list(self, **params):
        """Get a list of artists.

        Parameters:
            :param name: The name (or a fragment of the name) of the artist.
            :param order: Can be date or name.
            :param page: The page number.
        """
        return self._get('artist', params)

    def artist_create(self, name, urls=None, alias=None, group=None):
        """Function to create an artist (Requires login) (UNTESTED).

        Parameters:
            :param name: The artist's name.
            :param urls: A list of URLs associated with the artist, whitespace
                         delimited.
            :param alias: The artist that this artist is an alias for. Simply
                          enter the alias artist's name.
            :param group: The group or cicle that this artist is a member of.
                          Simply:param  enter the group's name.
        """
        params = {
            'artist[name]': name,
            'artist[urls]': urls,
            'artist[alias]': alias,
            'artist[group]': group
            }
        return self._get('artist/create', params, 'POST')

    def artist_update(self, artist_id, name=None, urls=None, alias=None,
                      group=None):
        """Function to update artists (Requires Login).

        Only the artist_id parameter is required. The other parameters are
        optional. (Requires login) (UNTESTED).

        Parameters:
            :param artist_id: The id of thr artist to update (Type: INT).
            :param name: The artist's name.
            :param urls: A list of URLs associated with the artist, whitespace
                         delimited.
            :param alias: The artist that this artist is an alias for. Simply
                          enter the alias artist's name.
            :param group: The group or cicle that this artist is a member of.
                          Simply enter the group's name.
        """
        params = {
            'id': artist_id,
            'artist[name]': name,
            'artist[urls]': urls,
            'artist[alias]': alias,
            'artist[group]': group
            }
        return self._get('artist/update', params, 'PUT')

    def artist_destroy(self, artist_id):
        """Action to lets you remove artist (Requires login) (UNTESTED).

        Parameters:
            :param artist_id: The id of the artist to destroy.
        """
        return self._get('artist/destroy', {'id': artist_id}, 'POST')

    def comment_show(self, comment_id):
        """Get a specific comment.

        Parameters:
            :param :param comment_id: The id number of the comment to retrieve.
        """
        return self._get('comment/show', {'id': comment_id})

    def comment_create(self, post_id, comment_body, anonymous=None):
        """Action to lets you create a comment (Requires login).

        Parameters:
            :param post_id: The post id number to which you are responding.
            :param comment_body: The body of the comment.
            :param anonymous: Set to 1 if you want to post this comment
                              anonymously.
        """
        if post_id and comment_body is not None:
            params = {
                'comment[post_id]': post_id,
                'comment[body]': comment_body,
                'comment[anonymous]': anonymous
                }
            return self._get('comment/create', params, 'POST')
        else:
            raise PybooruAPIError("Required 'post_id' and 'comment_body' "
                                  "parameters")

    def comment_destroy(self, comment_id):
        """Remove a specific comment (Requires login).

        Parameters:
            :param comment_id: The id number of the comment to remove.
        """
        return self._get('comment/destroy', {'id': comment_id}, 'DELETE')

    def wiki_list(self, **params):
        """Function to retrieves a list of every wiki page.

        Parameters:
            :param query: A word or phrase to search for (Default: None).
            :param order: Can be: title, date (Default: title).
            :param limit: The number of pages to retrieve (Default: 100).
            :param page: The page number.
        """
        return self._get('wiki', params)

    def wiki_create(self, title, body):
        """Action to lets you create a wiki page (Requires login) (UNTESTED).

        Parameters:
            :param title: The title of the wiki page.
            :param body: The body of the wiki page.
        """
        params = {'wiki_page[title]': title, 'wiki_page[body]': body}
        return self._get('wiki/create', params, 'POST')

    def wiki_update(self, page_title, new_title=None, page_body=None):
        """Action to lets you update a wiki page (Requires login) (UNTESTED).

        Parameters:
            :param page_title: The title of the wiki page to update.
            :param new_title: The new title of the wiki page.
            :param page_body: The new body of the wiki page.
        """
        params = {
            'title': page_title,
            'wiki_page[title]': new_title,
            'wiki_page[body]': page_body
            }
        return self._get('wiki/update', params, 'PUT')

    def wiki_show(self, **params):
        """Get a specific wiki page.

        Parameters:
            :param title: The title of the wiki page to retrieve.
            :param version: The version of the page to retrieve.
        """
        return self._get('wiki/show', params)

    def wiki_destroy(self, title):
        """Function to delete a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            :param title: The title of the page to delete.
        """
        return self._get('wiki/destroy', {'title': title}, 'DELETE')

    def wiki_lock(self, title):
        """Function to lock a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            :param title: The title of the page to lock.
        """
        return self._get('wiki/lock', {'title': title}, 'POST')

    def wiki_unlock(self, title):
        """Function to unlock a specific wiki page (Requires login)
        (Only moderators) (UNTESTED).

        Parameters:
            :param title: The title of the page to unlock.
        """
        return self._get('wiki/unlock', {'title': title}, 'POST')

    def wiki_revert(self, title, version):
        """Function to revert a specific wiki page (Requires login) (UNTESTED).

        Parameters:
            :param title: The title of the wiki page to update.
            :param version: The version to revert to.
        """
        params = {'title': title, 'version': version}
        return self._get('wiki/revert', params, 'PUT')

    def wiki_history(self, title):
        """Get history of specific wiki page.

        Parameters:
            :param title: The title of the wiki page to retrieve versions for.
        """
        return self._get('wiki/history', {'title': title})

    def note_list(self, **params):
        """Get note list.

        Parameters:
            :param post_id: The post id number to retrieve notes for.
        """
        return self._get('note', params)

    def note_search(self, query):
        """Search specific note.

        Parameters:
            :param query: A word or phrase to search for.
        """
        return self._get('note/search', {'query': query})

    def note_history(self, **params):
        """Get history of notes.

        Parameters:
            :param post_id: The post id number to retrieve note versions for.
            :param id: The note id number to retrieve versions for.
            :param limit: How many versions to retrieve (Default: 10).
            :param page: The note id number to retrieve versions for.
        """
        return self._get('note/history', params)

    def note_revert(self, note_id, version):
        """Function to revert a specific note (Requires login) (UNTESTED).

        Parameters:
            :param note_id: The note id to update.
            :param version: The version to revert to.
        """
        params = {'id': note_id, 'version': version}
        return self._get('note/revert', params, 'PUT')

    def note_create_update(self, post_id=None, coor_x=None, coor_y=None,
                           width=None, height=None, is_active=None, body=None,
                           note_id=None):
        """Function to create or update note (Requires login) (UNTESTED).

        Parameters:
            :param post_id: The post id number this note belongs to.
            :param coor_x: The X coordinate of the note.
            :param coor_y: The Y coordinate of the note.
            :param width: The width of the note.
            :param height: The height of the note.
            :param is_active: Whether or not the note is visible. Set to 1 for
                              active, 0 for inactive.
            :param body: The note message.
            :param note_id: If you are updating a note, this is the note id
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
        return self._get('note/update', params, 'POST')

    def user_search(self, **params):
        """Search users.

        If you don't specify any parameters you'll _get a listing of all users.

        Parameters:
            :param id: The id number of the user.
            :param name: The name of the user.
        """
        return self._get('user', params)

    def forum_list(self, **params):
        """Function to get forum posts.

        If you don't specify any parameters you'll _get a listing of all users.

        Parameters:
            :param parent_id: The parent ID number. You'll return all the
                              responses to that forum post.
        """
        return self._get('forum', params)

    def pool_list(self, **params):
        """Function to get pools.

        If you don't specify any parameters you'll _get a list of all pools.

        Parameters:
            :param query: The title.
            :param page: The page.
        """
        return self._get('pool', params)

    def pool_posts(self, **params):
        """Function to _get pools posts.

        If you don't specify any parameters you'll _get a list of all pools.

        Parameters:
            :param id: The pool id number.
            :param page: The page.
        """
        return self._get('pool/show', params)

    def pool_update(self, pool_id, name=None, is_public=None,
                    description=None):
        """Function to update a pool (Requires login) (UNTESTED).

        Parameters:
            :param pool_id: The pool id number.
            :param name: The name.
            :param is_public: 1 or 0, whether or not the pool is public.
            :param description: A description of the pool.
        """
        params = {
            'id': pool_id,
            'pool[name]': name,
            'pool[is_public]': is_public,
            'pool[description]': description
            }
        return self._get('pool/update', params, 'PUT')

    def pool_create(self, name, description, is_public):
        """Function to create a pool (Require login) (UNTESTED).

        Parameters:
            :param name: The name.
            :param description: A description of the pool.
            :param is_public: 1 or 0, whether or not the pool is public.
        """
        params = {'pool[name]': name, 'pool[description]': description,
                  'pool[is_public]': is_public}
        return self._get('pool/create', params, 'POST')

    def pool_destroy(self, pool_id):
        """Function to destroy a specific pool (Require login) (UNTESTED).

        Parameters:
            :param pool_id: The pool id number.
        """
        return self._get('pool/destroy', {'id': pool_id}, 'DELETE')

    def pool_add_post(self, **params):
        """Function to add a post (Require login) (UNTESTED).

        Parameters:
            :param pool_id: The pool to add the post to.
            :param post_id: The post to add.
        """
        return self._get('pool/add_post', params, 'PUT')

    def pool_remove_post(self, **params):
        """Function to remove a post (Require login) (UNTESTED).

        Parameters:
            :param pool_id: The pool to remove the post to.
            :param post_id: The post to remove.
        """
        return self._get('pool/remove_post', params, 'PUT')

    def favorite_list_users(self, post_id):
        """Function to return a list with all users who have added to favorites
        a specific post.

        Parameters:
            :param post_id: The post id.
        """
        response = self._get('favorite/list_users', {'id': post_id})
        # Return list with users
        return response['favorited_users'].split(',')
