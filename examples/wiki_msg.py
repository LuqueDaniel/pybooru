# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Pybooru

client = Pybooru('yandere')

wiki = client.wiki_list('nice', 'date', 2, 1)

for msg in wiki:
    print("Mensaje: {0}".format(msg['body']))
