# -*- coding: utf-8 -*-

"""pybooru.api_danbooru

This module contains all API calls of Gelbooru.

Classes:
    GelbooruApi_Mixin -- Contains all API endspoints.
"""

# __future__ imports
from __future__ import absolute_import

class GelbooruApi_Mixin(object):
    """Contains all Gelbooru API calls.
    * API Version commit: ?
    * Doc: https://gelbooru.me/index.php?page=wiki&s=view&id=18780
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            page (int): The page number starting at 1
            tags (str): The tags to search for. Any tag combination that works
                        on the web site will work here. This includes all the
                        meta-tags.
        """
        params['pid'] = params.pop('page')-1
        if( self.site_name == 'rule34'):
            return self._get_xml('post', params)
        return self._get('post', params)


    def tag_list(self, name_pattern=None, name=None, order=None, orderby=None):
        """Get a list of tags.

        Parameters:
            name_pattern (str): Can be: part or full name.
            name (str): Allows searching for tag with given name
            order (str): Can be: ASC, DESC.
            orderby (str): Can be: name, date, count.
        """
        params = {
            'name_pattern': name_pattern,
            'name': name,
            'order': order,
            'orderby': orderby
            }
        if( self.site_name == 'rule34'):
            return self._get_xml('tag', params)
        return self._get('tag', params)


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
