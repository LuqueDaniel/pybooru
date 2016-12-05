# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Moebooru

client = Moebooru('yandere')
wiki = client.wiki_list(query='nice', order='date', limit=2, page=1)

for msg in wiki:
    print("Mensaje: {0}".format(msg['body']))
