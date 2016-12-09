# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pybooru import Danbooru

client = Danbooru('danbooru')
tags = client.tag_list(order='date')

for tag in tags:
    print("Tag: {0} ----- {1}".format(tag['name'], tag['category']))
