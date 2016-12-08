# -*- coding: utf-8 -*-

"""pybooru.api_danbooru

This module contains all API calls of Danbooru.

Classes:
    DanbooruApi_Mixin -- Contains all API calls.
"""

# __future__ imports
from __future__ import absolute_import

# pybooru imports
from .exceptions import PybooruAPIError


class DanbooruApi_Mixin(object):
    """Contains all Danbooru API calls.

    * API Version: v2.105.0 (77e06b6)
    * Doc: https://danbooru.donmai.us/wiki_pages/43568
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            :param limit: How many posts you want to retrieve. There is a hard
                          limit of 100 posts per request.
            :param page: The page number.
            :param tags: The tags to search for. Any tag combination that works
                         on the web site will work here. This includes all the
                         meta-tags.
            :param raw: When this parameter is set the tags parameter will not
                        be parsed for aliased tags, metatags or multiple tags,
                        and will instead be parsed as a single literal tag.
        """
        return self._get('posts.json', params)

    def post_show(self, post_id):
        """Get a post.

        Parameters:
            :param post_id: REQUIRED Where post_id is the post id.
        """
        return self._get('/posts/{0}.json'.format(post_id))

    def post_update(self, post_id, tag_string=None, rating=None, source=None,
                    parent_id=None):
        """Update a specific post (Requires login).

        Parameters:
            :param post_id: REQUIRED The id number of the post to update.
            :param tag_string: A space delimited list of tags.
            :param rating: The rating for the post. Can be: safe, questionable,
                           or explicit.
            :param source: If this is a URL, Danbooru will download the file.
            :param parent_id: The ID of the parent post.
        """
        params = {
            'post[tag_string]': tag_string,
            'post[rating]': rating,
            'ost[source]': source,
            'post[parent_id]': parent_id
            }
        return self._get('/posts/{0}.json'.format(post_id), params, 'PUT',
                         auth=True)

    def post_revert(self, post_id, version_id):
        """Function to reverts a post to a previous version (Requires login).

        Parameters:
            :param post_id: REQUIRED post id.
            :param version_id: REQUIRED The post version id to revert to.
        """
        return self._get('/posts/{0}/revert.json'.format(post_id),
                         {'version_id': version_id}, 'PUT', auth=True)

    def post_copy_notes(self, post_id, other_post_id):
        """Function to copy notes (requires login).

        Parameters:
            :param post_id: REQUIRED Post id.
            :param other_post_id: REQUIRED The id of the post to copy notes to.
        """
        return self._get('/posts/{0}/copy_notes.json'.format(post_id),
                         {'other_post_id': other_post_id}, 'PUT', auth=True)

    def post_vote(self, post_id, score):
        """Action lets you vote for a post (Requires login).
        Danbooru: Post votes/create.

        Parameters:
            :param post_id: REQUIRED Ppost id.
            :param score: REQUIRED Can be: up, down.
        """
        return self._get('/posts/{0}/votes.json'.format(post_id),
                         {'score': score}, 'POST', auth=True)

    def post_flag_list(self, creator_id=None, creator_name=None, post_id=None,
                       reason_matches=None, is_resolved=None, category=None):
        """Function to flag a post (Requires login).

        Parameters:
            :param creator_id: The user id of the flag's creator.
            :param creator_name: The name of the flag's creator.
            :param post_id: The post id if the flag.
            :param reason_matches: Flag's reason.
            :param is_resolved: Can be 1 or 0.
            :param category: unapproved/banned/normal.
        """
        params = {
            'search[creator_id]': creator_id,
            'search[creator_name]': creator_name,
            'search[post_id]': post_id,
            'search[reason_matches]': reason_matches,
            'search[is_resolved]': is_resolved,
            'search[category]': category
            }
        return self._get('post_flags.json', params, auth=True)

    def post_flag_create(self, post_id, reason):
        """Function to flag a post.

        Parameters:
            :param post_id: REQUIRED The id of the flagged post.
            :param reason: REQUIRED The reason of the flagging.
        """
        params = {'post_flag[post_id]': post_id, 'post_flag[reason]': reason}
        return self._get('post_flags.json', params, 'POST', auth=True)

    def post_appeals_list(self, creator_id=None, creator_name=None,
                          post_id=None):
        """Function to return list of appeals (Requires login).

        Parameters:
            :param creator_id: The user id of the appeal's creator.
            :param creator_name: The name of the appeal's creator.
            :param post_id: The post id if the appeal.
        """
        params = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'post_id': post_id
            }
        return self._get('post_appeals.json', params, auth=True)

    def post_appeals_create(self, post_id, reason):
        """Function to create appeals (Requires login).

        Parameters:
            :param post_id: REQUIRED The id of the appealed post.
            :param reason: REQUIRED The reason of the appeal.
        """
        params = {'post_appeal[post_id]': post_id,
                  'post_appeal[reason]': reason}
        return self._get('post_appeals.json', params, 'POST', auth=True)

    def post_versions(self, updater_name=None, updater_id=None,
                      post_id=None, start_id=None):
        """Get list of post versions.

        Parameters:
            :param updater_name:
            :param updater_id:
            :param post_id:
            :param start_id:
        """
        params = {
            'search[updater_name]': updater_name,
            'search[updater_id]': updater_id,
            'search[post_id]': post_id,
            'search[start_id]': start_id
            }
        return self._get('post_versions.json', params)

    def upload_list(self, uploader_id=None, uploader_name=None, source=None):
        """Search and eturn a uploads list (Requires login).

        Parameters:
            :param uploader_id: The id of the uploader.
            :param uploader_name: The name of the uploader.
            :param source: The source of the upload (exact string match).
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
            :param upload_id: Where upload_id is the upload id.
        """
        return self._get('uploads/{0}.json'.format(upload_id), auth=True)

    def upload_create(self, tag_string, rating, file_=None, source=None,
                      parent_id=None):
        """Function to create a new upload (Requires login).

        Parameters:
            :param tag_string: REQUIRED The tags.
            :param rating: REQUIRED Can be: safe, questionable, explicit.
            :param file_: The file data encoded as a multipart form.
            :param source: The source URL.
            :param parent_id: The parent post id.
        """
        if file_ or source is not None:
            params = {
                'upload[source]': source,
                'upload[rating]': rating,
                'upload[parent_id]': parent_id,
                'upload[tag_string]': tag_string
                }
            file_ = {'upload[file]': open(file_, 'rb')}
            return self._get('uploads.json', params, 'POST', auth=True,
                             file_=file_)
        else:
            raise PybooruAPIError("'file_' or 'source' is required.")

    def comment_list(self, group_by, body_matches=None, post_id=None,
                     post_tags_match=None, creator_name=None, creator_id=None,
                     tags=None):
        """Return a list of comments.

        Parameters:
            :param group_by:
                Can be 'comment', 'post'. Comment will return recent comments.
                Post will return posts that have been recently commented on.

                :param group_by=comment:
                    :param body_matches: Body contains the given terms.
                    :param post_id: Post id.
                    :param post_tags_match: The comment's post's tags match
                                            the given terms.
                :param group_by=post:
                    :param tags: The post's tags match the given terms.
            :param creator_name: The name of the creator (exact match)
            :param creator_id: The user id of the creator
        """
        params = {'group_by': group_by}
        if group_by == 'comment':
            params['search[body_matches]'] = body_matches
            params['search[post_id]'] = post_id
            params['search[post_tags_match]'] = post_tags_match
            params['search[creator_name]'] = creator_name
            params['search[creator_id]'] = creator_id
        elif group_by == 'post':
            params['tags'] = tags
        else:
            raise PybooruAPIError("'group_by' must be 'comment' or post")
        return self._get('comments.json', params)

    def comment_create(self, post_id, body, do_not_bump_post=None):
        """Action to lets you create a comment (Requires login).

        Parameters:
            :param post_id: REQUIRED.
            :param body: REQUIRED.
            :param do_not_bump_post: Set to 1 if you do not want the post to be
                                     bumped to the top of the comment listing.
        """
        params = {
            'comment[post_id]': post_id,
            'comment[body]': body,
            'comment[do_not_bump_post]': do_not_bump_post
            }
        return self._get('comments.json', params, 'POST', auth=True)

    def comment_update(self, comment_id, body, do_not_bump_post=None):
        """Function to update a comment (Requires login).

        Parameters:
            :param comment_id: REQUIRED comment id.
            :param body: REQUIRED.
            :param do_not_bump_post: Set to 1 if you do not want the post to be
                                     bumped to the top of the comment listing.
        """
        params = {
            'comment[body]': body,
            'comment[do_not_bump_post]': do_not_bump_post
            }
        return self._get('comments/{0}.json'.format(comment_id), params, 'PUT',
                         auth=True)

    def comment_show(self, comment_id):
        """Get a specific comment.

        Parameters:
            :param comment_id: REQUIRED the id number of the comment to
                               retrieve.
        """
        return self._get('comments/{0}.json'.format(comment_id))

    def comment_delete(self, comment_id):
        """Remove a specific comment (Requires login).

        Parameters:
            :param comment_id: REQUIRED the id number of the comment to remove.
        """
        return self._get('comments/{0}.json'.format(comment_id),
                         method='DELETE', auth=True)

    def favorite_list(self, user_id=None):
        """Return a list with favorite posts (Requires login).

        Parameters:
            :param user_id: Which user's favorites to show. Defaults to your
                            own if not specified.
        """
        return self._get('favorites.json', {'user_id': user_id}, auth=True)

    def favorite_add(self, post_id):
        """Add post to favorite (Requires login).

        Parameters:
            :param post_id: REQUIRED The post to favorite.
        """
        return self._get('favorites.json', {'post_id': post_id}, 'POST',
                         auth=True)

    def favorite_remove(self, post_id):
        """Remove a post from favorites (Requires login).

        Parameters:
            :param post_id: REQUIRED where post_id is the post id.
        """
        return self._get('favorites/{0}.json'.format(post_id), method='DELETE',
                         auth=True)

    def dmail_list(self, message_matches=None, to_name=None, to_id=None,
                   from_name=None, from_id=None, read=None):
        """Return list of Dmails. You can only view dmails you own
        (Requires login).

        Parameters:
            :param message_matches: The message body contains the given terms.
            :param to_name: The recipient's name.
            :param to_id: The recipient's user id.
            :param from_name: The sender's name.
            :param from_id: The sender's user id.
            :param read: Can be: true, false.
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
            :param dmail_id: REQUIRED where dmail_id is the dmail id.
        """
        return self._get('dmails/{0}.json'.format(dmail_id), auth=True)

    def dmail_create(self, to_name, title, body):
        """Create a dmail (Requires login)

        Parameters:
            :param to_name: REQUIRED the recipient's name.
            :param title: REQUIRED the title of the message.
            :param body: REQUIRED the body of the message.
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
            :param dmail_id: REQUIRED where dmail_id is the dmail id.
        """
        return self._get('dmails/{0}.json'.format(dmail_id), method='DELETE',
                         auth=True)

    def artist_list(self, query=None, artist_id=None, creator_name=None,
                    creator_id=None, is_active=None, is_banned=None,
                    empty_only=None, order=None):
        """Get an artist of a list of artists.

        Parameters:
            :param query:
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
            :param artist_id: The artist id.
            :param creator_name: Exact creator name.
            :param creator_id: Artist creator id.
            :param is_active: Can be: true, false
            :param is_banned: Can be: true, false
            :param empty_only: Search for artists that have 0 posts. Can be:
                               true
            :param order: Can be: name, updated_at.
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
            :param artist_id:param : REQUIRED where artist_id is the artist id.
        """
        return self._get('artists/{0}.json'.format(artist_id))

    def artist_create(self, name, other_names_comma=None, group_name=None,
                      url_string=None):
        """Function to create an artist (Requires login) (UNTESTED).

        Parameters:
            :param name: REQUIRED.
            :param other_names_comma: List of alternative names for this
                                      artist, comma delimited.
            :param group_name: The name of the group this artist belongs to.
            :param url_string: List of URLs associated with this artist,
                               whitespace or newline delimited.
        """
        params = {
            'artist[name]': name,
            'artist[other_names_comma]': other_names_comma,
            'artist[group_name]': group_name,
            'artist[url_string]': url_string
            }
        return self.get('artists.json', params, method='POST', auth=True)

    def artist_update(self, artist_id, name=None, other_names_comma=None,
                      group_name=None, url_string=None):
        """Function to update artists (Requires login) (UNTESTED).

        Parameters:
            :param artist_id: REQUIRED where artist_id is the artist id.
            :param name:
            :param other_names_comma: List of alternative names for this
                                      artist, comma delimited.
            :param group_name: The name of the group this artist belongs to.
            :param url_string: List of URLs associated with this artist,
                               whitespace or newline delimited.
        """
        params = {
            'artist[name]': name,
            'artist[other_names_comma]': other_names_comma,
            'artist[group_name]': group_name,
            'artist[url_string]': url_string
            }
        return self .get('artists/{0}.json'.format(artist_id), params,
                         method='PUT', auth=True)

    def artist_delete(self, artist_id):
        """Action to lets you delete an artist (Requires login) (UNTESTED).

        Parameters:
            :param artist_id: where artist_id is the artist id.
        """
        return self._get('artists/{0}.json'.format(artist_id), method='DELETE',
                         auth=True)

    def artist_banned(self):
        """This is a shortcut for an artist listing search with
        name=status:banned.:param """
        return self._get('artists/banned.json')

    def artist_revert(self, artist_id, version_id):
        """Revert an artist (Requires login) (UNTESTED).

        Parameters:
            :param artist_id: REQUIRED The artist id.
            :param version_id: REQUIRED The artist version id to revert to.
        """
        params = {'version_id': version_id}
        return self._get('artists/{0}/revert.json'.format(artist_id), params,
                         method='PUT', auth=True)

    def artist_versions(self, name=None, updater_id=None, artist_id=None,
                        is_active=None, is_banned=None, order=None):
        """Get list of artist versions.

        Parameters:
            :param name:
            :param updater_id:
            :param artist_id:
            :param is_active: Can be: true, false.
            :param is_banned: Can be: true, false.
            :param order: Can be: name, date.
        """
        params = {
            'search[name]': name,
            'search[updater_id]': updater_id,
            'search[artist_id]': artist_id,
            'search[is_active]': is_active,
            'search[is_banned]': is_banned,
            'search[order]': order
            }
        return self._get('artist_versions.json', params)

    def artist_commentary_list(self, text_matches=None, post_id=None,
                               post_tags_match=None, original_present=None,
                               translated_present=None):
        """list artist commentary.

        Parameters:
            :param text_matches:
            :param post_id:
            :param post_tags_match: The commentary's post's tags match the
                                    giventerms. Meta-tags not supported.
            :param original_present: Can be: yes, no.
            :param translated_present: Can be: yes, no.
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
            :param post_id: REQUIRED.
            :param original_title:
            :param original_description:
            :param translated_title:
            :param translated_description:
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
            :param id_: REQUIRED The artist commentary id.
            :param version_id: REQUIRED The artist commentary version id to
                               revert to.
        """
        params = {'version_id': version_id}
        return self._get('artist_commentaries/{0}/revert.json'.format(id_),
                         params, method='PUT', auth=True)

    def artist_commentary_versions(self, post_id, updater_id):
        """Return list of artist commentary versions.

        Parameters:
            :param updater_id: REQUIRED.
            :param post_id: REQUIRED.
        """
        params = {
            'search[updater_id]': updater_id,
            'search[post_id]': post_id
            }
        return self._get('artist_commentary_versions.json', params)

    def note_list(self, group_by=None, body_matches=None, post_id=None,
                  post_tags_match=None, creator_name=None, creator_id=None):
        """Return list of notes.

        Parameters:
            :param group_by: Can be: note, post (by default post).
            :param body_matches: The note's body matches the given terms.
            :param post_id: A specific post.
            :param post_tags_match: The note's post's tags match the given
                                    terms.
            :param creator_name: The creator's name. Exact match.
            :param creator_id: The creator's user id.
        """
        params = {
            'group_by': group_by,
            'search[body_matches]': body_matches,
            'search[post_id]': post_id,
            'search[post_tags_match]': post_tags_match,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id
            }
        return self._get('notes.json', params)

    def note_show(self, note_id):
        """Get a specific note.

        Parameters:
            :param :param note_id: REQUIRED Where note_id is the note id.
        """
        return self._get('notes/{0}.json'.format(note_id))

    def note_create(self, post_id, coor_x, coor_y, width, height, body):
        """Function to create a note (Requires login) (UNTESTED).

        Parameters:
            :param post_id: REQUIRED
            :param coor_x: REQUIRED The x coordinates of the note in pixels,
                           with respect to the top-left corner of the image.
            :param coor_y: REQUIRED The y coordinates of the note in pixels,
                           with respect to the top-left corner of the image.
            :param width: REQUIRED The width of the note in pixels.
            :param height: REQUIRED The height of the note in pixels.
            :param body: REQUIRED The body of the note.
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
            :param note_id: REQUIRED Where note_id is the note id.
            :param coor_x: REQUIRED The x coordinates of the note in pixels,
                           with respect to the top-left corner of the image.
            :param coor_y: REQUIRED The y coordinates of the note in pixels,
                           with respect to the top-left corner of the image.
            :param width: REQUIRED The width of the note in pixels.
            :param height: REQUIRED The height of the note in pixels.
            :param body: REQUIRED The body of the note.
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
            :param note_id: REQUIRED Where note_id is the note id.
        """
        return self._get('notes/{0}.json'.format(note_id), method='DELETE',
                         auth=True)

    def note_revert(self, note_id, version_id):
        """Function to revert a specific note (Requires login) (UNTESTED).

        Parameters:
            :param note_id: REQUIRED Where note_id is the note id.
            :param version_id: REQUIRED The note version id to revert to.
        """
        return self._get('notes/{0}/revert.json'.format(note_id),
                         {'version_id': version_id}, method='PUT', auth=True)

    def note_versions(self, updater_id=None, post_id=None, note_id=None):
        """Get list of note versions.

        Parameters:
            :param updater_id:
            :param post_id:
            :param note_id:
        """
        params = {
            'search[updater_id]': updater_id,
            'search[post_id]': post_id,
            'search[note_id]': note_id
            }
        return self._get('note_versions.json', params)

    def user_list(self, name=None, min_level=None, max_level=None, level=None,
                  user_id=None, order=None):
        """Function to get a list of users or a specific user.

        Levels:
            Users have a number attribute called level representing their role.
            The current levels are:

            Member 20, Gold 30, Platinum 31, Builder 32, Contributor 33,
            Janitor 35, Moderator 40 and Admin 50.

        Parameters:
            :param name: Supports patterns.
            :param min_level: Minimum level (see section on levels).
            :param max_level: Maximum level (see section on levels).
            :param level: Current level (see section on levels).
            :param user_id: The user id.
            :param order: Can be: 'name', 'post_upload_count', 'note_count',
                          'post_update_count', 'date'.
        """
        params = {
            'search[name]': name,
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
            :param user_id: REQUIRED Where user_id is the user id.
        """
        return self._get('users/{0}.json'.format(user_id))

    def pool_list(self, name_matches=None, description_matches=None,
                  creator_name=None, creator_id=None, is_active=None,
                  order=None, category=None):
        """Get a list of pools.

        Parameters:
            :param name_matches:
            :param description_matches:
            :param creator_name:
            :param creator_id:
            :param is_active: Can be: true, false.
            :param order: Can be: name, created_at, post_count, date.
            :param category: Can be: series, collection
        """
        params = {
            'search[name_matches]': name_matches,
            'search[description_matches]': description_matches,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id,
            'search[is_active]': is_active,
            'search[order]': order,
            'search[category]': category
            }
        return self._get('pools.json', params)

    def pool_show(self, pool_id):
        """Get a specific pool.

        Parameters:
            :param pool_id: REQUIRED Where pool_id is the pool id.
        """
        return self._get('pools/{0}.json'.format(pool_id))

    def pool_create(self, name, description, category):
        """Function to create a pool (Requires login) (UNTESTED).

        Parameters:
            :param name: REQUIRED.
            :param description: REQUIRED.
            :param category: Can be: series, collection.
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
            :param pool_id: REQUIRED Where pool_id is the pool id.
            :param name:
            :param description:
            :param post_ids: List of space delimited post ids.
            :param is_active: Can be: 1, 0
            :param category: Can be: series, collection
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
        """Delete a pool (Requires login) (UNTESTED).

        Parameters:
            :param pool_id: REQUIRED Where pool_id is the pool id.
        """
        return self._get('pools/{0}.json'.format(pool_id), method='DELETE',
                         auth=True)

    def pool_undelete(self, pool_id):
        """Undelete a specific poool (Requires login) (UNTESTED).

        Parameters:
            :param pool_id: REQUIRED Where pool_id is the pool id.
        """
        return self._get('pools/{0}/undelete.json'.format(pool_id),
                         method='POST', auth=True)

    def pool_revert(self, pool_id, version_id):
        """Function to revert a specific pool (Requires login) (UNTESTED).

        Parameters:
            :param pool_id: REQUIRED Where pool_id is the pool id.
            :param version_id: REQUIRED.
        """
        params = {'version_id': version_id}
        return self._get('pools/{0}/revert.json'.format(pool_id), params,
                         method='PUT', auth=True)

    def pool_versions(self, updater_id=None, updater_name=None, pool_id=None):
        """Get list of pool versions.

        Parameters:
            :param updater_id:
            :param updater_name:
            :param pool_id:
        """
        params = {
            'search[updater_id]': updater_id,
            'search[updater_name]': updater_name,
            'search[pool_id]': pool_id
            }
        return self._get('pool_versions.json', params)

    def tag_list(self, name_matches=None, category=None, hide_empty=None,
                 order=None, has_wiki=None, name=None):
        """Get a list of tags.

        Parameters:
            :param name_matches:
            :param category: Can be: 0, 1, 3, 4 (general, artist, copyright,
                             character respectively)
            :param hide_empty: Can be: yes, no. Excludes tags with 0 posts
                               when "yes".
            :param order: Can be: name, date, count
            :param has_wiki: Can be: yes, no
            :param name: Allows searching for multiple tags with exact given
                         names, separated by commas. e.g.
                         search[name]=touhou,original,k-on! would return the
                         three listed tags.
        """
        params = {
            'search[name_matches]': name_matches,
            'search[category]': category,
            'search[hide_empty]': hide_empty,
            'search[order]': order,
            'search[has_wiki]': has_wiki,
            'search[name]': name
            }
        return self._get('tags.json', params)

    def tag_aliases(self, name_matches=None, antecedent_name=None,
                    tag_id=None):
        """Get tags aliases.

        Parameters:
            :param name_matches: Match antecedent or consequent name.
            :param antecedent_name: Match antecedent name (exact match).
            :param tag_id: The tag alias id.
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
            :param name_matches: Match antecedent or consequent name.
            :param antecedent_name: Match antecedent name (exact match).
            :param tag_id: The tag implication id.
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
            :param query: REQUIRED The tag to find the related tags for.
            :param category: If specified, show only tags of a specific
                             category. Can be: General 0, Artist 1, Copyright
                             3 and Character 4.
        """
        params = {'query': query, 'category': category}
        return self._get('related_tag.json', params)

    def wiki_list(self, title=None, creator_id=None, body_matches=None,
                  other_names_match=None, creator_name=None, order=None):
        """Function to retrieves a list of every wiki page.

        Parameters:
            :param title:
            :param creator_id:
            :param body_matches:
            :param other_names_match:
            :param creator_name:
            :param order: Can be: date, title.
        """
        params = {
            'search[title]': title,
            'search[creator_id]': creator_id,
            'search[body_matches]': body_matches,
            'search[other_names_match]': other_names_match,
            'search[creator_name]': creator_name,
            'search[order]': order
            }
        return self._get('wiki_pages.json', params)

    def wiki_show(self, wiki_page_id):
        """Retrieve a specific page of the wiki.

        Parameters:
            :param wiki_page_id: REQUIRED Where page_id is the wiki page id.
        """
        return self._get('wiki_pages/{0}.json'.format(wiki_page_id))

    def wiki_create(self, title, body, other_names=None):
        """Action to lets you create a wiki page (Requires login) (UNTESTED).

        Parameters:
            :param title: REQUIRED.
            :param body: REQUIRED.
            :param other_names:
        """
        params = {
            'wiki_page[title]': title,
            'wiki_page[body]': body,
            'wiki_page[other_names]': other_names
            }
        return self._get('wiki_pages.json', params, method='POST', auth=True)

    def wiki_update(self, wiki_page_id, title=None, body=None,
                    other_names=None):
        """Action to lets you update a wiki page (Requires login) (UNTESTED).

        Parameters:
            :param wiki_page_id: REQURIED Whre page_id is the wiki page id.
            :param title:
            :param body:
            :param other_names:
        """
        params = {
            'wiki_page[title]': title,
            'wiki_page[body]': body,
            'wiki_page[other_names]': other_names
            }
        return self._get('wiki_pages/{0}.json'.format(wiki_page_id), params,
                         method='PUT', auth=True)

    def wiki_revert(self, wiki_page_id, version_id):
        """Revert page to a previeous version (Requires login) (UNTESTED).

        Parameters:
            :param wiki_page_id: REQUIRED Where page_id is the wiki page id.
            :param version_id: REQUIRED.
        """
        return self._get('wiki_pages/{0}/revert.json'.format(wiki_page_id),
                         {'version_id': version_id}, method='PUT', auth=True)

    def wiki_versions(self, wiki_page_id, updater_id):
        """Return a list of wiki page version.

        Parameters:
            :param wiki_page_id: REQUIRED.
            :param updater_id: REQUIRED.
        """
        params = {
            'earch[updater_id]': updater_id,
            'search[wiki_page_id]': wiki_page_id
            }
        return self._get('wiki_page_versions.json', params)

    def wiki_versions_show(self, wiki_page_id):
        """Return a specific wiki page version.

        Parameters:
            :param wiki_page_id: REQUIRED Where wiki_page_id is the wiki page
                                 version id.
        """
        return self._get('wiki_page_versions/{0}.json'.format(wiki_page_id))

    def forum_topic_list(self, title_matches=None, title=None,
                         category_id=None):
        """Function to get forum topics.

        Parameters:
            :param title_matches: Search body for the given terms.
            :param title: Exact title match.
            :param category_id: Can be: 0, 1, 2 (General, Tags, Bugs & Features
                                respectively)
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
            :param topic_id: REQUIRED Where topic_id is the forum topic id.
        """
        return self._get('forum_topics/{0}.json'.format(topic_id))

    def forum_topic_create(self, title, body, category=None):
        """Function to create topic (Requires login) (UNTESTED).

        Parameters:
            :param title: topic title.
            :param body: Message of the initial post.
            :param category: Can be: 0, 1, 2 (General, Tags, Bugs & Features
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
            :param topic_id: REQUIRED .ñWhere topic_id is the topic id.
            :param title: Topic title.
            :param category: Can be: 0, 1, 2 (General, Tags, Bugs & Features
                             respectively)
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
            :param topic_id: REQUIRED Where topic_id is the topic id.
        """
        return self._get('forum_topics/{0}.json'.format(topic_id),
                         method='DELETE', auth=True)

    def forum_topic_undelete(self, topic_id):
        """Un delete a topic (Login requries) (Moderator+) (UNTESTED).

        Parameters:
            :param topic_id: REQUIRED Where topic_id is the topic id.
        """
        return self._get('forum_topics/{0}/undelete.json'.format(topic_id),
                         method='POST', auth=True)

    def forum_post_list(self, creator_id=None, creator_name=None,
                        topic_id=None, topic_title_matches=None,
                        topic_category_id=None, body_matches=None):
        """Return a list of forum posts.

        Parameters:
            :param creator_id:
            :param creator_name:
            :param topic_id:
            :param topic_title_matches:
            :param topic_category_id: Can be: 0, 1, 2 (General, Tags, Bugs &
                                      Features respectively)
            :param body_matches:
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
            :param topic_id: REQUIRED.
            :param body: REQUIRED.
        """
        params = {
            'forum_post[topic_id]': topic_id,
            'forum_post[body]': body
            }
        return self._get('forum_posts.json', params, method='POST', auth=True)

    def forum_post_update(self, topic_id, body):
        """Update a specific forum post (Requries login)(Moderator+)(UNTESTED).

        Parameters:
            :param post_id: REQUIRED Forum topic id.
            :param body: REQUIRED.
        """
        params = {'forum_post[body]': body}
        return self._get('forum_posts/{0}.json'.format(topic_id), params,
                         method='PUT', auth=True)

    def forum_post_delete(self, post_id):
        """Delete a specific forum post (Requires login)(Moderator+)(UNTESTED).

        Parameters:
            :param post_id: REQUIRED forum post id.
        """
        return self._get('forum_posts/{0}.json'.format(post_id),
                         method='DELETE', auth=True)

    def forum_post_undelete(self, post_id):
        """Undelete a specific forum post (Requires login) (Moderator+)
           (UNTESTED).

        Parameters:
            :param post_id: REQUIRED forum post id.
        """
        return self._get('forum_posts/{0}/undelete.json'.format(post_id),
                         method='POST', auth=True)
