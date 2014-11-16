# -*- coding: utf-8 -*-

from pybooru import Pybooru

client = Pybooru('Konachan')

tags = client.tags_list(None, None, 100, 0, 'date')

for tag in tags:
    print("Nombre: {0} ----- {1}".format(tag['name'], tag['type']))
