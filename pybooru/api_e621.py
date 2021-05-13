# -*- coding: utf-8 -*-

"""pybooru.api_danbooru

This module contains all API calls of E621.

Classes:
    E621Api_Mixin -- Contains all API endspoints.
"""

# __future__ imports
from __future__ import absolute_import

class E621Api_Mixin(object):
    """Contains all E621 API calls.
    * API Version commit: ?
    * Doc: https://e621.net/help/api#posts
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            page (int): The page number.
            tags (str): The tags to search for. Any tag combination that works
                        on the web site will work here. This includes all the
                        meta-tags.
        """

        return self._get('posts.json', params)


    def tag_list(self, name=None, category=None, order=None, hide_empty=None, has_wiki=None, has_artist=None, extra_params={}):
        """Get a list of tags.

        Parameters:
            name_matches (str): A tag name expression to match against
            category (int): Filters results to a particular category
            order (str): date/count/name
            has_wiki (str): Show only tags with wiki, true/false
            has_artist (str): true/false

        """
        params = {
            'search[name_matches]': name,
            'search[category]': category,
            'search[order]': order,
            'search[hide_empty]': hide_empty,
            'search[has_wiki]': has_wiki,
            'search[has_artist]': has_artist,
            }
        params.update(extra_params)
        return self._get('tags.json', params)



    def artist_list(self, query=None, artist_id=None, creator_name=None,
                    creator_id=None, any_name_matches=None, is_active=None,
                    empty_only=None, order=None, is_banned=None, extra_params={}):
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
            'search[any_name_matches]': any_name_matches,
            'search[creator_id]': creator_id,
            'search[is_active]': is_active,
            'search[is_banned]': is_banned,
            'search[empty_only]': empty_only,
            'search[order]': order
            }
        params.update(extra_params)
        return self._get('artists.json', params)

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
