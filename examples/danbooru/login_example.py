# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Danbooru

client = Danbooru('danbooru', username='your-username', api_key='yout-api_key')
response = client.comment_create(post_id=id, body='your comment')

print(client.last_call)
