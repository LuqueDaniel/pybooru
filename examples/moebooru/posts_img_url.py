# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Moebooru

client = Moebooru('Konachan')
posts = client.post_list(tags='blue_eyes', limit=10)

for post in posts:
    print("URL image: {0}".format(post['file_url']))
