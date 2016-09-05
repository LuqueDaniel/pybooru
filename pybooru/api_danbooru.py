# -*- coding: utf-8 -*-

"""pybooru.api_danbooru

This module contains all API calls of Danbooru for Pybooru.

Classes:
    Danbooru -- Contains all API calls.
"""

# __future__ imports
from __future__ import absolute_import

# pybooru imports
from .exceptions import PybooruAPIError


class DanbooruApi(object):
    """Contains all Danbooru API calls.

    API Versions: v2.105.0
    doc: https://danbooru.donmai.us/wiki_pages/43568
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            limit: How many posts you want to retrieve. There is a hard limit
                   of 100 posts per request.
            page: The page number.
            tags: The tags to search for. Any tag combination that works on the
                  web site will work here. This includes all the meta-tags.
            raw: When this parameter is set the tags parameter will not be
                 parsed for aliased tags, metatags or multiple tags, and will
                 instead be parsed as a single literal tag.
        """
        return self._get('posts.json', params)

    def post_show(self, id_):
        """Get a post.

        Parameters:
            id_: REQUIRED Where id_ is the post id.
        """
        return self._get('/posts/{0}.json'.format(id_))

    def post_update(self, id_, tag_string=None, rating=None, source=None,
                    parent_id=None):
        """Update a specific post (Requires login).

        Parameters:
            id_: REQUIRED The id number of the post to update.
            tag_string: A space delimited list of tags.
            rating: The rating for the post. Can be: safe, questionable, or
                    explicit.
            source: If this is a URL, Danbooru will download the file.
            parent_id: The ID of the parent post.
        """
        params = {
            'post[tag_string]': tag_string,
            'post[rating]': rating,
            'ost[source]': source,
            'post[parent_id]': parent_id
            }
        return self._get('/posts/{0}.json'.format(id_), params, 'PUT',
                         auth=True)

    def post_revert(self, id_, version_id):
        """Function to reverts a post to a previous version (Requires login).

        Parameters:
            id_: REQUIRED post id.
            version_id: REQUIRED The post version id to revert to.
        """
        return self._get('/posts/{0}/revert.json'.format(id_),
                         {'version_id': version_id}, 'PUT', auth=True)

    def post_copy_notes(self, id_, other_post_id):
        """Function to copy notes (requires login).

        Parameters:
            id_: REQUIRED Post id.
            other_post_id: REQUIRED The id of the post to copy notes to.
        """
        return self._get('/posts/{0}/copy_notes.json'.format(id_),
                         {'other_post_id': other_post_id}, 'PUT', auth=True)

    def post_vote(self, id_, score):
        """Action lets you vote for a post (Requires login).
        Danbooru: Post votes/create

        Parameters:
            id_: REQUIRED Ppost id.
            score: REQUIRED Can be: up, down.
        """
        return self._get('/posts/{0}/votes.json'.format(id_), {'score': score},
                         'POST', auth=True)

    def post_flag_list(self, creator_id=None, creator_name=None, post_id=None,
                       reason_matches=None, is_resolved=None, category=None):
        """Function to flag a post (Requires login).

        Parameters:
            creator_id: The user id of the flag's creator.
            creator_name: The name of the flag's creator.
            post_id: The post id if the flag.
            reason_matches: Flag's reason.
            is_resolved:
            category: unapproved/banned/normal.
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

    def post_flag_create(self, id_, reason):
        """Function to flag a post.

        Parameters:
            id_: REQUIRED The id of the flagged post.
            reason: REQUIRED The reason of the flagging.
        """
        params = {'post_flag[post_id]': id_, 'post_flag[reason]': reason}
        return self._get('post_flags.json', params, 'POST', auth=True)

    def post_appeals_list(self, creator_id=None, creator_name=None,
                          post_id=None):
        """Function to return list of appeals (Requires login).

        Parameters:
            creator_id: The user id of the appeal's creator.
            creator_name: The name of the appeal's creator.
            post_id: The post id if the appeal.
        """
        params = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'post_id': post_id
            }
        return self._get('post_appeals.json', params, auth=True)

    def post_appeals_create(self, id_, reason):
        """Function to create appeals (Requires login).

        Parameters:
            id_: REQUIRED The id of the appealed post.
            reason: REQUIRED The reason of the appeal.
        """
        params = {
            'post_appeal[post_id]': id_,
            'post_appeal[reason]': reason
            }
        return self._get('post_appeals.json', params, 'POST', auth=True)

    def upload_list(self, uploader_id=None, uploader_name=None, source=None):
        """Search and eturn a uploads list (Requires login).

        Parameters:
            uploader_id: The id of the uploader.
            uploader_name: The name of the uploader.
            source The: source of the upload (exact string match).
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
            upload_id: Where upload_id is the upload id.
        """
        return self._get('uploads/{0}.json'.format(upload_id), auth=True)

    def upload_create(self, tag_string, rating, file_=None, source=None,
                      parent_id=None):
        """Function to create a new upload (Requires login).

        Parameters:
            tag_string: REQUIRED The tags.
            rating: REQUIRED Can be: safe, questionable, explicit.
            file_: The file data encoded as a multipart form.
            source: The source URL.
            parent_id: The parent post id.
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
