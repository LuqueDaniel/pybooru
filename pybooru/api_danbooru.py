# -*- coding: utf-8 -*-

"""pybooru.api_danbooru

This module contains all API calls of Danbooru.

Classes:
    DanbooruApi_Mixin -- Contains all API endspoints.
"""

# __future__ imports
from __future__ import absolute_import

# pybooru imports
from .exceptions import PybooruAPIError


class DanbooruApi_Mixin(object):
    """Contains all Danbooru API calls.

    * API Version commit: 9996030
    * Doc: https://danbooru.donmai.us/wiki_pages/43568
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            limit (int): How many posts you want to retrieve. There is a hard
                         limit of 100 posts per request.
            page (int): The page number.
            tags (str): The tags to search for. Any tag combination that works
                        on the web site will work here. This includes all the
                        meta-tags.
            md5 (str): The md5 of the image to search for.
            random (bool): Can be: True, False.
            raw (bool): When this parameter is set the tags parameter will not
                        be parsed for aliased tags, metatags or multiple tags,
                        and will instead be parsed as a single literal tag.
        """
        return self._get('posts.json', params)

    def post_show(self, post_id):
        """Get a post.

        Parameters:
            post_id (int): Where post_id is the post id.
        """
        return self._get('posts/{0}.json'.format(post_id))

    def post_update(self, post_id, tag_string=None, rating=None, source=None,
                    parent_id=None, has_embedded_notes=None,
                    is_rating_locked=None, is_note_locked=None,
                    is_status_locked=None):
        """Update a specific post (Requires login).

        Parameters:
            post_id (int): The id number of the post to update.
            tag_string (str): A space delimited list of tags.
            rating (str): The rating for the post. Can be: safe, questionable,
                          or explicit.
            source (str): If this is a URL, Danbooru will download the file.
            parent_id (int): The ID of the parent post.
            has_embedded_notes (int): Can be 1, 0.
            is_rating_locked (int): Can be: 0, 1 (Builder+ only).
            is_note_locked (int): Can be: 0, 1 (Builder+ only).
            is_status_locked (int): Can be: 0, 1 (Admin only).
        """
        params = {
            'post[tag_string]': tag_string,
            'post[rating]': rating,
            'ost[source]': source,
            'post[parent_id]': parent_id,
            'post[has_embedded_notes]': has_embedded_notes,
            'post[is_rating_locked]': is_rating_locked,
            'post[is_note_locked]': is_note_locked,
            'post[is_status_locked]': is_status_locked
            }
        return self._get('posts/{0}.json'.format(post_id), params, 'PUT',
                         auth=True)

    def post_revert(self, post_id, version_id):
        """Function to reverts a post to a previous version (Requires login).

        Parameters:
            post_id (int):
            version_id (int): The post version id to revert to.
        """
        return self._get('posts/{0}/revert.json'.format(post_id),
                         {'version_id': version_id}, 'PUT', auth=True)

    def post_copy_notes(self, post_id, other_post_id):
        """Function to copy notes (requires login).

        Parameters:
            post_id (int):
            other_post_id (int): The id of the post to copy notes to.
        """
        return self._get('posts/{0}/copy_notes.json'.format(post_id),
                         {'other_post_id': other_post_id}, 'PUT', auth=True)

    def post_mark_translated(self, post_id, check_translation,
                             partially_translated):
        """Mark post as translated (Requires login) (UNTESTED).

        If you set check_translation and partially_translated to 1 post will
        be tagged as 'translated_request'

        Parameters:
            post_id (int):
            check_translation (int): Can be 0, 1.
            partially_translated (int): Can be 0, 1
        """
        param = {
            'post[check_translation]': check_translation,
            'post[partially_translated]': partially_translated
            }
        return self._get('posts/{0}/mark_as_translated.json'.format(post_id),
                         param, method='PUT', auth=True)

    def post_vote(self, post_id, score):
        """Action lets you vote for a post (Requires login).
        Danbooru: Post votes/create.

        Parameters:
            post_id (int):
            score (str): Can be: up, down.
        """
        return self._get('posts/{0}/votes.json'.format(post_id),
                         {'score': score}, 'POST', auth=True)

    def post_unvote(self, post_id):
        """Action lets you unvote for a post (Requires login).

        Parameters:
            post_id (int):
        """
        return self._get('posts/{0}/unvote.json'.format(post_id),
                         method='PUT', auth=True)

    def post_flag_list(self, creator_id=None, creator_name=None, post_id=None,
                       reason_matches=None, is_resolved=None, category=None):
        """Function to flag a post (Requires login).

        Parameters:
            creator_id (int): The user id of the flag's creator.
            creator_name (str): The name of the flag's creator.
            post_id (int): The post id if the flag.
        """
        params = {
            'search[creator_id]': creator_id,
            'search[creator_name]': creator_name,
            'search[post_id]': post_id,
            }
        return self._get('post_flags.json', params, auth=True)

    def post_flag_show(self, flag_id):
        """Show specific flagged post (Requires login).

        Parameters:
            flag_id (int):
        """
        return self._get('post_appeals/{0}.json'.format(flag_id), auth=True)

    def post_flag_create(self, post_id, reason):
        """Function to flag a post.

        Parameters:
            post_id (int): The id of the flagged post.
            reason (str): The reason of the flagging.
        """
        params = {'post_flag[post_id]': post_id, 'post_flag[reason]': reason}
        return self._get('post_flags.json', params, 'POST', auth=True)

    def post_appeals_list(self, creator_id=None, creator_name=None,
                          post_id=None):
        """Function to return list of appeals (Requires login).

        Parameters:
            creator_id (int): The user id of the appeal's creator.
            creator_name (str): The name of the appeal's creator.
            post_id (int): The post id if the appeal.
        """
        params = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'post_id': post_id
            }
        return self._get('post_appeals.json', params, auth=True)

    def post_appeals_show(self, appeal_id):
        """Show a specific post appeal (Requires login) (UNTESTED).

        Parameters:
            appeal_id:
        """
        return self._get('post_appeals/{0}.json'.format(appeal_id), auth=True)

    def post_appeals_create(self, post_id, reason):
        """Function to create appeals (Requires login).

        Parameters:
            post_id (int): The id of the appealed post.
            reason (str) The reason of the appeal.
        """
        params = {'post_appeal[post_id]': post_id,
                  'post_appeal[reason]': reason}
        return self._get('post_appeals.json', params, 'POST', auth=True)

    def post_versions_list(self, updater_name=None, updater_id=None,
                           post_id=None, start_id=None):
        """Get list of post versions.

        Parameters:
            updater_name (str):
            updater_id (int):
            post_id (int):
            start_id (int):
        """
        params = {
            'search[updater_name]': updater_name,
            'search[updater_id]': updater_id,
            'search[post_id]': post_id,
            'search[start_id]': start_id
            }
        return self._get('post_versions.json', params)

    def post_versions_show(self, version_id):
        """Show a specific post version (UNTESTED).

        Parameters:
            version_id (int):
        """
        return self._get('post_versions/{0}.json'.format(version_id))

    def post_versions_undo(self, version_id):
        """Undo post version (Requires login) (UNTESTED).

        Parameters:
            version_id (int):
        """
        return self._get('post_versions/{0}/undo.json'.format(version_id),
                         method='PUT', auth=True)

    def upload_list(self, uploader_id=None, uploader_name=None, source=None):
        """Search and eturn a uploads list (Requires login).

        Parameters:
            uploader_id (int): The id of the uploader.
            uploader_name (str): The name of the uploader.
            source (str): The source of the upload (exact string match).
        """
        params = {
            'search[uploader_id]': uploader_id,
            'search[uploader_name]': uploader_name,
            'search[source]': source
            }
        return self._get('uploads.json', params, auth=True)

    def upload_show(self, upload_id):
        """Get a upload (Requires login).

        Parameters:
            upload_id (int):
        """
        return self._get('uploads/{0}.json'.format(upload_id), auth=True)

    def upload_create(self, tags, rating, file_=None, source=None,
                      parent_id=None):
        """Function to create a new upload (Requires login).

        Parameters:
            tags (str):
            rating (str): Can be: safe, questionable, explicit.
            file_ (file_path): The file data encoded as a multipart form.
            source (str): The source URL.
            parent_id (int): The parent post id.

        Raises:
            PybooruAPIError: When file_ or source are empty.
        """
        if file_ or source is not None:
            params = {
                'upload[source]': source,
                'upload[rating]': rating,
                'upload[parent_id]': parent_id,
                'upload[tag_string]': tags
                }
            file_ = {'upload[file]': open(file_, 'rb')}
            return self._get('uploads.json', params, 'POST', auth=True,
                             file_=file_)
        else:
            raise PybooruAPIError("'file_' or 'source' is required.")

    def comment_list(self, group_by, limit=None, page=None, body_matches=None,
                     post_id=None, post_tags_match=None, creator_name=None,
                     creator_id=None, is_deleted=None):
        """Return a list of comments.

        Parameters:
            limit (int): How many posts you want to retrieve.
            page (int): The page number.
            group_by: Can be 'comment', 'post'. Comment will return recent
                      comments. Post will return posts that have been recently
                      commented on.
            body_matches (str): Body contains the given terms.
            post_id (int):
            post_tags_match (str): The comment's post's tags match the
                                   given terms. Meta-tags not supported.
            creator_name (str): The name of the creator (exact match).
            creator_id (int): The user id of the creator.
            is_deleted (bool): Can be: True, False.

        Raises:
            PybooruAPIError: When 'group_by' is invalid.
        """
        params = {
            'group_by': group_by,
            'limit': limit,
            'page': page,
            'search[body_matches]': body_matches,
            'search[post_id]': post_id,
            'search[post_tags_match]': post_tags_match,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id,
            'search[is_deleted]': is_deleted
            }
        return self._get('comments.json', params)

    def comment_create(self, post_id, body, do_not_bump_post=None):
        """Action to lets you create a comment (Requires login).

        Parameters:
            post_id (int):
            body (str):
            do_not_bump_post (bool): Set to 1 if you do not want the post to be
                                     bumped to the top of the comment listing.
        """
        params = {
            'comment[post_id]': post_id,
            'comment[body]': body,
            'comment[do_not_bump_post]': do_not_bump_post
            }
        return self._get('comments.json', params, 'POST', auth=True)

    def comment_update(self, comment_id, body):
        """Function to update a comment (Requires login).

        Parameters:
            comment_id (int):
            body (str):
        """
        params = {'comment[body]': body}
        return self._get('comments/{0}.json'.format(comment_id), params, 'PUT',
                         auth=True)

    def comment_show(self, comment_id):
        """Get a specific comment.

        Parameters:
            comment_id (int): The id number of the comment to retrieve.
        """
        return self._get('comments/{0}.json'.format(comment_id))

    def comment_delete(self, comment_id):
        """Remove a specific comment (Requires login).

        Parameters:
            comment_id (int): The id number of the comment to remove.
        """
        return self._get('comments/{0}.json'.format(comment_id),
                         method='DELETE', auth=True)

    def comment_undelete(self, comment_id):
        """Undelete a specific comment (Requires login) (UNTESTED).

        Parameters:
            comment_id (int):
        """
        return self._get('comments/{0}/undelete.json'.format(comment_id),
                         method='POST', auth=True)

    def comment_vote(self, comment_id, score):
        """Lets you vote for a comment (Requires login).

        Parameters:
            comment_id (int):
            score (str): Can be: up, down.
        """
        params = {'score': score}
        return self._get('comments/{0}/votes.json'.format(comment_id), params,
                         method='POST', auth=True)

    def comment_unvote(self, comment_id):
        """Lets you unvote a specific comment (Requires login).

        Parameters:
            comment_id (int):
        """
        return self._get('posts/{0}/unvote.json'.format(comment_id),
                         method='POST', auth=True)

    def favorite_list(self, user_id=None):
        """Return a list with favorite posts (Requires login).

        Parameters:
            user_id (int): Which user's favorites to show. Defaults to your own
                           if not specified.
        """
        return self._get('favorites.json', {'user_id': user_id}, auth=True)

    def favorite_add(self, post_id):
        """Add post to favorite (Requires login).

        Parameters:
            post_id (int): The post to favorite.
        """
        return self._get('favorites.json', {'post_id': post_id}, 'POST',
                         auth=True)

    def favorite_remove(self, post_id):
        """Remove a post from favorites (Requires login).

        Parameters:
            post_id (int): Where post_id is the post id.
        """
        return self._get('favorites/{0}.json'.format(post_id), method='DELETE',
                         auth=True)

    def dmail_list(self, message_matches=None, to_name=None, to_id=None,
                   from_name=None, from_id=None, read=None):
        """Return list of Dmails. You can only view dmails you own
        (Requires login).

        Parameters:
            message_matches (str): The message body contains the given terms.
            to_name (str): The recipient's name.
            to_id (int): The recipient's user id.
            from_name (str): The sender's name.
            from_id (int): The sender's user id.
            read (bool): Can be: true, false.
        """
        params = {
            'search[message_matches]': message_matches,
            'search[to_name]': to_name,
            'search[to_id]': to_id,
            'search[from_name]': from_name,
            'search[from_id]': from_id,
            'search[read]': read
            }
        return self._get('dmails.json', params, auth=True)

    def dmail_show(self, dmail_id):
        """Return a specific dmail. You can only view dmails you own
        (Requires login).

        Parameters:
            dmail_id (int): Where dmail_id is the dmail id.
        """
        return self._get('dmails/{0}.json'.format(dmail_id), auth=True)

    def dmail_create(self, to_name, title, body):
        """Create a dmail (Requires login)

        Parameters:
            to_name (str): The recipient's name.
            title (str): The title of the message.
            body (str): The body of the message.
        """
        params = {
            'dmail[to_name]': to_name,
            'dmail[title]': title,
            'dmail[body]': body
            }
        return self._get('dmails.json', params, 'POST', auth=True)

    def dmail_delete(self, dmail_id):
        """Delete a dmail. You can only delete dmails you own (Requires login).

        Parameters:
            dmail_id (int): where dmail_id is the dmail id.
        """
        return self._get('dmails/{0}.json'.format(dmail_id), method='DELETE',
                         auth=True)

    def artist_list(self, query=None, artist_id=None, creator_name=None,
                    creator_id=None, is_active=None, is_banned=None,
                    empty_only=None, order=None):
        """Get an artist of a list of artists.

        Parameters:
            query (str):
                This field has multiple uses depending on what the query starts
                with:
                'http:desired_url':
                    Search for artist with this URL.
                'name:desired_url':
                    Search for artists with the given name as their base name.
                'other:other_name':
                    Search for artists with the given name in their other
                    names.
                'group:group_name':
                    Search for artists belonging to the group with the given
                    name.
                'status:banned':
                    Search for artists that are banned. else Search for the
                    given name in the base name and the other names.
            artist_id (id): The artist id.
            creator_name (str): Exact creator name.
            creator_id (id): Artist creator id.
            is_active (bool): Can be: true, false
            is_banned (bool): Can be: true, false
            empty_only (True): Search for artists that have 0 posts. Can be:
                               true
            order (str): Can be: name, updated_at.
        """
        params = {
            'search[name]': query,
            'search[id]': artist_id,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id,
            'search[is_active]': is_active,
            'search[is_banned]': is_banned,
            'search[empty_only]': empty_only,
            'search[order]': order
            }
        return self._get('artists.json', params)

    def artist_show(self, artist_id):
        """Return a specific artist.

        Parameters:
            artist_id (int): Where artist_id is the artist id.
        """
        return self._get('artists/{0}.json'.format(artist_id))

    def artist_create(self, name, other_names_comma=None, group_name=None,
                      url_string=None, body=None):
        """Function to create an artist (Requires login) (UNTESTED).

        Parameters:
            name (str):
            other_names_comma (str): List of alternative names for this
                                     artist, comma delimited.
            group_name (str): The name of the group this artist belongs to.
            url_string (str): List of URLs associated with this artist,
                              whitespace or newline delimited.
            body (str): DText that will be used to create a wiki entry at the
                        same time.
        """
        params = {
            'artist[name]': name,
            'artist[other_names_comma]': other_names_comma,
            'artist[group_name]': group_name,
            'artist[url_string]': url_string,
            'artist[body]': body,
            }
        return self.get('artists.json', params, method='POST', auth=True)

    def artist_update(self, artist_id, name=None, other_names_comma=None,
                      group_name=None, url_string=None, body=None):
        """Function to update artists (Requires login) (UNTESTED).

        Parameters:
            artist_id (str):
            name (str): Artist name.
            other_names_comma (str): List of alternative names for this
                                     artist, comma delimited.
            group_name (str): The name of the group this artist belongs to.
            url_string (str): List of URLs associated with this artist,
                              whitespace or newline delimited.
            body (str): DText that will be used to create/update a wiki entry
                        at the same time.
        """
        params = {
            'artist[name]': name,
            'artist[other_names_comma]': other_names_comma,
            'artist[group_name]': group_name,
            'artist[url_string]': url_string,
            'artist[body]': body
            }
        return self .get('artists/{0}.json'.format(artist_id), params,
                         method='PUT', auth=True)

    def artist_delete(self, artist_id):
        """Action to lets you delete an artist (Requires login) (UNTESTED)
        (Only Builder+).

        Parameters:
            artist_id (int): Where artist_id is the artist id.
        """
        return self._get('artists/{0}.json'.format(artist_id), method='DELETE',
                         auth=True)

    def artist_undelete(self, artist_id):
        """Lets you undelete artist (Requires login) (UNTESTED) (Only Builder+).

        Parameters:
            artist_id (int):
        """
        return self._get('artists/{0}/undelete.json'.format(artist_id),
                         method='POST', auth=True)

    def artist_banned(self):
        """This is a shortcut for an artist listing search with
        name=status:banned."""
        return self._get('artists/banned.json')

    def artist_revert(self, artist_id, version_id):
        """Revert an artist (Requires login) (UNTESTED).

        Parameters:
            artist_id (int): The artist id.
            version_id (int): The artist version id to revert to.
        """
        params = {'version_id': version_id}
        return self._get('artists/{0}/revert.json'.format(artist_id), params,
                         method='PUT', auth=True)

    def artist_versions(self, name=None, updater_name=None, updater_id=None,
                        artist_id=None, is_active=None, is_banned=None,
                        order=None):
        """Get list of artist versions (Requires login).

        Parameters:
            name (str):
            updater_name (str):
            updater_id (int):
            artist_id (int):
            is_active (bool): Can be: True, False.
            is_banned (bool): Can be: True, False.
            order (str): Can be: name (Defaults to ID)
        """
        params = {
            'search[name]': name,
            'search[updater_name]': updater_name,
            'search[updater_id]': updater_id,
            'search[artist_id]': artist_id,
            'search[is_active]': is_active,
            'search[is_banned]': is_banned,
            'search[order]': order
            }
        return self._get('artist_versions.json', params, auth=True)

    def artist_commentary_list(self, text_matches=None, post_id=None,
                               post_tags_match=None, original_present=None,
                               translated_present=None):
        """list artist commentary.

        Parameters:
            text_matches (str):
            post_id (int):
            post_tags_match (str): The commentary's post's tags match the
                                   giventerms. Meta-tags not supported.
            original_present (str): Can be: yes, no.
            translated_present (str): Can be: yes, no.
        """
        params = {
            'search[text_matches]': text_matches,
            'search[post_id]': post_id,
            'search[post_tags_match]': post_tags_match,
            'search[original_present]': original_present,
            'search[translated_present]': translated_present
            }
        return self._get('artist_commentaries.json', params)

    def artist_commentary_create_update(self, post_id, original_title,
                                        original_description, translated_title,
                                        translated_description):
        """Create or update artist commentary (Requires login) (UNTESTED).

        Parameters:
            post_id (int): Post id.
            original_title (str): Original title.
            original_description (str): Original description.
            translated_title (str): Translated title.
            translated_description (str): Translated description.
        """
        params = {
            'artist_commentary[post_id]': post_id,
            'artist_commentary[original_title]': original_title,
            'artist_commentary[original_description]': original_description,
            'artist_commentary[translated_title]': translated_title,
            'artist_commentary[translated_description]': translated_description
            }
        return self._get('artist_commentaries/create_or_update.json', params,
                         method='POST', auth=True)

    def artist_commentary_revert(self, id_, version_id):
        """Revert artist commentary (Requires login) (UNTESTED).

        Parameters:
            id_ (int): The artist commentary id.
            version_id (int): The artist commentary version id to
                              revert to.
        """
        params = {'version_id': version_id}
        return self._get('artist_commentaries/{0}/revert.json'.format(id_),
                         params, method='PUT', auth=True)

    def artist_commentary_versions(self, post_id, updater_id):
        """Return list of artist commentary versions.

        Parameters:
            updater_id (int):
            post_id (int):
        """
        params = {'search[updater_id]': updater_id, 'search[post_id]': post_id}
        return self._get('artist_commentary_versions.json', params)

    def note_list(self, body_matches=None, post_id=None, post_tags_match=None,
                  creator_name=None, creator_id=None, is_active=None):
        """Return list of notes.

        Parameters:
            body_matches (str): The note's body matches the given terms.
            post_id (int): A specific post.
            post_tags_match (str): The note's post's tags match the given terms.
            creator_name (str): The creator's name. Exact match.
            creator_id (int): The creator's user id.
            is_active (bool): Can be: True, False.
        """
        params = {
            'search[body_matches]': body_matches,
            'search[post_id]': post_id,
            'search[post_tags_match]': post_tags_match,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id,
            'search[is_active]': is_active
            }
        return self._get('notes.json', params)

    def note_show(self, note_id):
        """Get a specific note.

        Parameters:
            note_id (int): Where note_id is the note id.
        """
        return self._get('notes/{0}.json'.format(note_id))

    def note_create(self, post_id, coor_x, coor_y, width, height, body):
        """Function to create a note (Requires login) (UNTESTED).

        Parameters:
            post_id (int):
            coor_x (int): The x coordinates of the note in pixels,
                          with respect to the top-left corner of the image.
            coor_y (int): The y coordinates of the note in pixels,
                          with respect to the top-left corner of the image.
            width (int): The width of the note in pixels.
            height (int): The height of the note in pixels.
            body (str): The body of the note.
        """
        params = {
            'note[post_id]': post_id,
            'note[x]': coor_x,
            'note[y]': coor_y,
            'note[width]': width,
            'note[height]': height,
            'note[body]': body
            }
        return self._get('notes.json', params, method='POST', auth=True)

    def note_update(self, note_id, coor_x=None, coor_y=None, width=None,
                    height=None, body=None):
        """Function to update a note (Requires login) (UNTESTED).

        Parameters:
            note_id (int): Where note_id is the note id.
            coor_x (int): The x coordinates of the note in pixels,
                          with respect to the top-left corner of the image.
            coor_y (int): The y coordinates of the note in pixels,
                          with respect to the top-left corner of the image.
            width (int): The width of the note in pixels.
            height (int): The height of the note in pixels.
            body (str): The body of the note.
        """
        params = {
            'note[x]': coor_x,
            'note[y]': coor_y,
            'note[width]': width,
            'note[height]': height,
            'note[body]': body
            }
        return self._get('notes/{0}.jso'.format(note_id), params, method='PUT',
                         auth=True)

    def note_delete(self, note_id):
        """delete a specific note (Requires login) (UNTESTED).

        Parameters:
            note_id (int): Where note_id is the note id.
        """
        return self._get('notes/{0}.json'.format(note_id), method='DELETE',
                         auth=True)

    def note_revert(self, note_id, version_id):
        """Function to revert a specific note (Requires login) (UNTESTED).

        Parameters:
            note_id (int): Where note_id is the note id.
            version_id (int): The note version id to revert to.
        """
        return self._get('notes/{0}/revert.json'.format(note_id),
                         {'version_id': version_id}, method='PUT', auth=True)

    def note_versions(self, updater_id=None, post_id=None, note_id=None):
        """Get list of note versions.

        Parameters:
            updater_id (int):
            post_id (int):
            note_id (int):
        """
        params = {
            'search[updater_id]': updater_id,
            'search[post_id]': post_id,
            'search[note_id]': note_id
            }
        return self._get('note_versions.json', params)

    def user_list(self, name=None, name_matches=None, min_level=None,
                  max_level=None, level=None, user_id=None, order=None):
        """Function to get a list of users or a specific user.

        Levels:
            Users have a number attribute called level representing their role.
            The current levels are:

            Member 20, Gold 30, Platinum 31, Builder 32, Contributor 33,
            Janitor 35, Moderator 40 and Admin 50.

        Parameters:
            name (str): Supports patterns.
            name_matches (str): Same functionality as name.
            min_level (int): Minimum level (see section on levels).
            max_level (int): Maximum level (see section on levels).
            level (int): Current level (see section on levels).
            user_id (int): The user id.
            order (str): Can be: 'name', 'post_upload_count', 'note_count',
                         'post_update_count', 'date'.
        """
        params = {
            'search[name]': name,
            'search[name_matches]': name_matches,
            'search[min_level]': min_level,
            'search[max_level]': max_level,
            'search[level]': level,
            'search[id]': user_id,
            'search[order]': order
            }
        return self._get('users.json', params)

    def user_show(self, user_id):
        """Get a specific user.

        Parameters:
            user_id (int): Where user_id is the user id.
        """
        return self._get('users/{0}.json'.format(user_id))

    def pool_list(self, name_matches=None, pool_ids=None, category=None,
                  description_matches=None, creator_name=None, creator_id=None,
                  is_deleted=None, is_active=None, order=None):
        """Get a list of pools.

        Parameters:
            name_matches (str):
            pool_ids (str): Can search for multiple ID's at once, separated by
                           commas.
            description_matches (str):
            creator_name (str):
            creator_id (int):
            is_active (bool): Can be: true, false.
            is_deleted (bool): Can be: True, False.
            order (str): Can be: name, created_at, post_count, date.
            category (str): Can be: series, collection.
        """
        params = {
            'search[name_matches]': name_matches,
            'search[id]': pool_ids,
            'search[description_matches]': description_matches,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id,
            'search[is_active]': is_active,
            'search[is_deleted]': is_deleted,
            'search[order]': order,
            'search[category]': category
            }
        return self._get('pools.json', params)

    def pool_show(self, pool_id):
        """Get a specific pool.

        Parameters:
            pool_id (int): Where pool_id is the pool id.
        """
        return self._get('pools/{0}.json'.format(pool_id))

    def pool_create(self, name, description, category):
        """Function to create a pool (Requires login) (UNTESTED).

        Parameters:
            name (str): Pool name.
            description (str): Pool description.
            category (str): Can be: series, collection.
        """
        params = {
            'pool[name]': name,
            'pool[description]': description,
            'pool[category]': category
            }
        return self._get('pools.json', params, method='POST', auth=True)

    def pool_update(self, pool_id, name=None, description=None, post_ids=None,
                    is_active=None, category=None):
        """Update a pool (Requires login) (UNTESTED).

        Parameters:
            pool_id (int): Where pool_id is the pool id.
            name (str):
            description (str):
            post_ids (str): List of space delimited post ids.
            is_active (int): Can be: 1, 0.
            category (str): Can be: series, collection.
        """
        params = {
            'pool[name]': name,
            'pool[description]': description,
            'pool[post_ids]': post_ids,
            'pool[is_active]': is_active,
            'pool[category]': category
            }
        return self._get('pools/{0}.json'.format(pool_id), params,
                         method='PUT', auth=True)

    def pool_delete(self, pool_id):
        """Delete a pool (Requires login) (UNTESTED) (Moderator+).

        Parameters:
            pool_id (int): Where pool_id is the pool id.
        """
        return self._get('pools/{0}.json'.format(pool_id), method='DELETE',
                         auth=True)

    def pool_undelete(self, pool_id):
        """Undelete a specific poool (Requires login) (UNTESTED) (Moderator+).

        Parameters:
            pool_id (int): Where pool_id is the pool id.
        """
        return self._get('pools/{0}/undelete.json'.format(pool_id),
                         method='POST', auth=True)

    def pool_revert(self, pool_id, version_id):
        """Function to revert a specific pool (Requires login) (UNTESTED).

        Parameters:
            pool_id (int): Where pool_id is the pool id.
            version_id (int):
        """
        return self._get('pools/{0}/revert.json'.format(pool_id),
                         {'version_id': version_id}, method='PUT', auth=True)

    def pool_versions(self, updater_id=None, updater_name=None, pool_id=None):
        """Get list of pool versions.

        Parameters:
            updater_id (int):
            updater_name (str):
            pool_id (int):
        """
        params = {
            'search[updater_id]': updater_id,
            'search[updater_name]': updater_name,
            'search[pool_id]': pool_id
            }
        return self._get('pool_versions.json', params)

    def tag_list(self, name_matches=None, name=None, category=None,
                 hide_empty=None, has_wiki=None, has_artist=None, order=None):
        """Get a list of tags.

        Parameters:
            name_matches (str): Can be: part or full name.
            name (str): Allows searching for multiple tags with exact given
                        names, separated by commas. e.g.
                        search[name]=touhou,original,k-on! would return the
                        three listed tags.
            category (str): Can be: 0, 1, 3, 4 (general, artist, copyright,
                            character respectively).
            hide_empty (str): Can be: yes, no. Excludes tags with 0 posts
                              when "yes".
            has_wiki (str): Can be: yes, no.
            has_artist (str): Can be: yes, no.
            order (str): Can be: name, date, count.
        """
        params = {
            'search[name_matches]': name_matches,
            'search[name]': name,
            'search[category]': category,
            'search[hide_empty]': hide_empty,
            'search[has_wiki]': has_wiki,
            'search[has_artist]': has_artist,
            'search[order]': order
            }
        return self._get('tags.json', params)

    def tag_show(self, tag_id):
        """Show a specific tag.

        Parameters:
            tag_id (int):
        """
        return self._get('tags/{0}.json'.format(tag_id))

    def tag_update(self, tag_id, category):
        """Lets you update a tag (Requires login) (UNTESTED).

        Parameters:
            tag_id (int):
            category (str): Can be: 0, 1, 3, 4 (general, artist, copyright,
                            character respectively).
        """
        param = {'tag[category]': category}
        return self._get('pools/{0}.json'.format(tag_id), param, method='PUT',
                         auth=True)

    def tag_aliases(self, name_matches=None, antecedent_name=None,
                    tag_id=None):
        """Get tags aliases.

        Parameters:
            name_matches (str): Match antecedent or consequent name.
            antecedent_name (str): Match antecedent name (exact match).
            tag_id (int): The tag alias id.
        """
        params = {
            'search[name_matches]': name_matches,
            'search[antecedent_name]': antecedent_name,
            'search[id]': tag_id
            }
        return self._get('tag_aliases.json', params)

    def tag_implications(self, name_matches=None, antecedent_name=None,
                         tag_id=None):
        """Get tags implications.

        Parameters:
            name_matches (str): Match antecedent or consequent name.
            antecedent_name (str): Match antecedent name (exact match).
            tag_id (int): Tag implication id.
        """
        params = {
            'search[name_matches]': name_matches,
            'search[antecedent_name]': antecedent_name,
            'search[id]': tag_id
            }
        return self._get('tag_implications.json', params)

    def tag_related(self, query, category=None):
        """Get related tags.

        Parameters:
            query (str): The tag to find the related tags for.
            category (str): If specified, show only tags of a specific
                            category. Can be: General 0, Artist 1, Copyright
                            3 and Character 4.
        """
        params = {'query': query, 'category': category}
        return self._get('related_tag.json', params)

    def wiki_list(self, title=None, creator_id=None, body_matches=None,
                  other_names_match=None, creator_name=None, hide_deleted=None,
                  other_names_present=None, order=None):
        """Function to retrieves a list of every wiki page.

        Parameters:
            title (str): Page title.
            creator_id (int): Creator id.
            body_matches (str): Page content.
            other_names_match (str): Other names.
            creator_name (str): Creator name.
            hide_deleted (str): Can be: yes, no.
            other_names_present (str): Can be: yes, no.
            order (str): Can be: date, title.
        """
        params = {
            'search[title]': title,
            'search[creator_id]': creator_id,
            'search[body_matches]': body_matches,
            'search[other_names_match]': other_names_match,
            'search[creator_name]': creator_name,
            'search[hide_deleted]': hide_deleted,
            'search[other_names_present]': other_names_present,
            'search[order]': order
            }
        return self._get('wiki_pages.json', params)

    def wiki_show(self, wiki_page_id):
        """Retrieve a specific page of the wiki.

        Parameters:
            wiki_page_id (int): Where page_id is the wiki page id.
        """
        return self._get('wiki_pages/{0}.json'.format(wiki_page_id))

    def wiki_create(self, title, body, other_names=None):
        """Action to lets you create a wiki page (Requires login) (UNTESTED).

        Parameters:
            title (str): Page title.
            body (str): Page content.
            other_names (str): Other names.
        """
        params = {
            'wiki_page[title]': title,
            'wiki_page[body]': body,
            'wiki_page[other_names]': other_names
            }
        return self._get('wiki_pages.json', params, method='POST', auth=True)

    def wiki_update(self, page_id, title=None, body=None,
                    other_names=None, is_locked=None, is_deleted=None):
        """Action to lets you update a wiki page (Requires login) (UNTESTED).

        Parameters:
            page_id (int): Whre page_id is the wiki page id.
            title (str): Page title.
            body (str): Page content.
            other_names (str): Other names.
            is_locked (int): Can be: 0, 1 (Builder+).
            is_deleted (int): Can be: 0, 1 (Builder+).
        """
        params = {
            'wiki_page[title]': title,
            'wiki_page[body]': body,
            'wiki_page[other_names]': other_names
            }
        return self._get('wiki_pages/{0}.json'.format(page_id), params,
                         method='PUT', auth=True)

    def wiki_delete(self, page_id):
        """Delete a specific page wiki (Requires login) (UNTESTED) (Builder+).

        Parameters:
            page_id (int):
        """
        return self._get('wiki_pages/{0}.json'.format(page_id), auth=True,
                         method='DELETE')

    def wiki_revert(self, wiki_page_id, version_id):
        """Revert page to a previeous version (Requires login) (UNTESTED).

        Parameters:
            wiki_page_id (int): Where page_id is the wiki page id.
            version_id (int):
        """
        return self._get('wiki_pages/{0}/revert.json'.format(wiki_page_id),
                         {'version_id': version_id}, method='PUT', auth=True)

    def wiki_versions_list(self, page_id, updater_id):
        """Return a list of wiki page version.

        Parameters:
            page_id (int):
            updater_id (int):
        """
        params = {
            'earch[updater_id]': updater_id,
            'search[wiki_page_id]': page_id
            }
        return self._get('wiki_page_versions.json', params)

    def wiki_versions_show(self, page_id):
        """Return a specific wiki page version.

        Parameters:
            page_id (int): Where page_id is the wiki page version id.
        """
        return self._get('wiki_page_versions/{0}.json'.format(page_id))

    def forum_topic_list(self, title_matches=None, title=None,
                         category_id=None):
        """Function to get forum topics.

        Parameters:
            title_matches (str): Search body for the given terms.
            title (str): Exact title match.
            category_id (int): Can be: 0, 1, 2 (General, Tags, Bugs & Features
                               respectively).
        """
        params = {
            'search[title_matches]': title_matches,
            'search[title]': title,
            'search[category_id]': category_id
            }
        return self._get('forum_topics.json', params)

    def forum_topic_show(self, topic_id):
        """Retrieve a specific forum topic.

        Parameters:
            topic_id (int): Where topic_id is the forum topic id.
        """
        return self._get('forum_topics/{0}.json'.format(topic_id))

    def forum_topic_create(self, title, body, category=None):
        """Function to create topic (Requires login) (UNTESTED).

        Parameters:
            title (str): topic title.
            body (str): Message of the initial post.
            category (str): Can be: 0, 1, 2 (General, Tags, Bugs & Features
                            respectively).
        """
        params = {
            'forum_topic[title]': title,
            'forum_topic[original_post_attributes][body]': body,
            'forum_topic[category_id]': category
            }
        return self._get('forum_topics.json', params, method='POST', auth=True)

    def forum_topic_update(self, topic_id, title=None, category=None):
        """Update a specific topic (Login Requires) (UNTESTED).

        Parameters:
            topic_id (int): Where topic_id is the topic id.
            title (str): Topic title.
            category (str): Can be: 0, 1, 2 (General, Tags, Bugs & Features
                            respectively).
        """
        params = {
            'forum_topic[title]': title,
            'forum_topic[category_id]': category
            }
        return self._get('forum_topics/{0}.json'.format(topic_id), params,
                         method='PUT', auth=True)

    def forum_topic_delete(self, topic_id):
        """Delete a topic (Login Requires) (Moderator+) (UNTESTED).

        Parameters:
            topic_id (int): Where topic_id is the topic id.
        """
        return self._get('forum_topics/{0}.json'.format(topic_id),
                         method='DELETE', auth=True)

    def forum_topic_undelete(self, topic_id):
        """Un delete a topic (Login requries) (Moderator+) (UNTESTED).

        Parameters:
            topic_id (int): Where topic_id is the topic id.
        """
        return self._get('forum_topics/{0}/undelete.json'.format(topic_id),
                         method='POST', auth=True)

    def forum_post_list(self, creator_id=None, creator_name=None,
                        topic_id=None, topic_title_matches=None,
                        topic_category_id=None, body_matches=None):
        """Return a list of forum posts.

        Parameters:
            creator_id (int):
            creator_name (str):
            topic_id (int):
            topic_title_matches (str):
            topic_category_id (int): Can be: 0, 1, 2 (General, Tags, Bugs &
                                     Features respectively).
            body_matches (str): Can be part of the post content.
        """
        params = {
            'search[creator_id]': creator_id,
            'search[creator_name]': creator_name,
            'search[topic_id]': topic_id,
            'search[topic_title_matches]': topic_title_matches,
            'search[topic_category_id]': topic_category_id,
            'search[body_matches]': body_matches
            }
        return self._get('forum_posts.json', params)

    def forum_post_create(self, topic_id, body):
        """Create a forum post (Requires login).

        Parameters:
            topic_id (int):
            body (str): Post content.
        """
        params = {'forum_post[topic_id]': topic_id, 'forum_post[body]': body}
        return self._get('forum_posts.json', params, method='POST', auth=True)

    def forum_post_update(self, topic_id, body):
        """Update a specific forum post (Requries login)(Moderator+)(UNTESTED).

        Parameters:
            post_id (int): Forum topic id.
            body (str): Post content.
        """
        params = {'forum_post[body]': body}
        return self._get('forum_posts/{0}.json'.format(topic_id), params,
                         method='PUT', auth=True)

    def forum_post_delete(self, post_id):
        """Delete a specific forum post (Requires login)(Moderator+)(UNTESTED).

        Parameters:
            post_id (int): Forum post id.
        """
        return self._get('forum_posts/{0}.json'.format(post_id),
                         method='DELETE', auth=True)

    def forum_post_undelete(self, post_id):
        """Undelete a specific forum post (Requires login)(Moderator+)(UNTESTED).

        Parameters:
            post_id (int): Forum post id.
        """
        return self._get('forum_posts/{0}/undelete.json'.format(post_id),
                         method='POST', auth=True)
