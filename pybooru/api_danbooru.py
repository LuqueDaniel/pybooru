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
