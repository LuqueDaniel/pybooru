# -*- coding: utf-8 -*-

from pybooru import Pybooru

client = Pybooru('Konachan')

posts = client.posts_list('blue_eyes', 10)

for post in posts:
    print("URL imagen: {0}".format(post['file_url']))
