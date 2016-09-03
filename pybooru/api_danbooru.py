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
        """Get a post

        Parameters:
            id_: where id_ is the post id.
        """
        return self._get("/posts/{0}.json".format(id_))
