Pybooru - Library for Danbooru API
========================================================================
Pybooru is a library for Python for access to API Danbooru based sites.

Version: **1.4.9**<br />
Licensed under: **MIT License**

Installation
------------------------------------------------------------------------
For installation Pybooru

``` shell
    git clone git://github.com/luquedaniel/pybooru.git
    cd pybooru
    sudo python setup.py install
```

Example use.
------------------------------------------------------------------------
``` python
from Pybooru import Pybooru

client = Pybooru('Konachan')

artists = client.artists('ma')

for artist in artists:
	print 'Name: %s' % (artist['name'])
```

Special Thanks to
------------------------------------------------------------------------
