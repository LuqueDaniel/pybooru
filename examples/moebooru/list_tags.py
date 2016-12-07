# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Moebooru

client = Moebooru('Konachan')
tags = client.tag_list(order='name')

for tag in tags:
    print("Tag: {0} ----- {1}".format(tag['name'], tag['type']))
