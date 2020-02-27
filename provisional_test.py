# encoding: utf-8
from __future__ import print_function
from pybooru import Danbooru
from pybooru import Moebooru

konachan = Moebooru("konachan")

kona_tags = konachan.tag_list(order='date')
print(konachan.last_call)
kona_post = konachan.post_list()
print(konachan.last_call)

lolibooru = Moebooru("lolibooru")

kona_tags = lolibooru.tag_list(order='date')
print(lolibooru.last_call)
kona_post = lolibooru.post_list()
print(lolibooru.last_call)

danbooru = Danbooru('danbooru')

dan_tags = danbooru.tag_list(order='name')
print(danbooru.last_call)
dan_post = danbooru.post_list(tags="computer")
print(danbooru.last_call)
