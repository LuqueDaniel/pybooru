# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Moebooru

client = Moebooru(site_name='Konachan')

# notes = client.note_list()
# print(notes)

# wiki = client.wiki_list(query='nice', order='date')
# for msg in wiki:
#    print("Mensaje: {0}".format(msg['body']))

# posts = client.post_list(tags='blue_eyes', limit=2)
# for post in posts:
#    print("URL imagen: {0}".format(post['file_url']))

# tags = client.tag_list()
# for tag in tags:
#    print("Nombre: {0} ----- {1}".format(tag['name'], tag['type']))
