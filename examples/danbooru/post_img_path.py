# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Danbooru

client = Danbooru('danbooru')
posts = client.post_list(tags='blue_eyes', limit=5)

for post in posts:
    print("Image path: {0}".format(post['file_url']))
