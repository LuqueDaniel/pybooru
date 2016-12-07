# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Moebooru

client = Moebooru('yandere')
wiki = client.wiki_list(body_matches='great', order='date')

for page in wiki:
    print("Message: {0}".format(page['body']))
