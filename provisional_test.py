# encoding: utf-8
from pybooru import Pybooru

# client = Pybooru(site_url='konachan.com')
client = Pybooru(site_url="http://www.konachan.com")

tags = client.tag_list(order='date')
