# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Moebooru

# replace login information
client = Moebooru('Konachan', username='your-username', password='your-password')
client.comment_create(post_id=id, comment_body='Comment content')
