# encoding: utf-8
from __future__ import print_function
from pybooru import Pybooru

# client = Pybooru(site_url='konachan.com')
client = Pybooru(site_url="http://www.konachan.com")

tags = client.tag_list(order='date')
print(client.last_call)
posts = client.post_list()
print(client.last_call)
