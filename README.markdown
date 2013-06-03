Pybooru - Library for Danbooru API.
========================================================================
Pybooru is a library for Python for access to API Danbooru based sites.

Version: **2.0**<br />
Licensed under: **MIT License**

Installation.
------------------------------------------------------------------------
For installation Pybooru.

```bash
    git clone git://github.com/luquedaniel/pybooru.git
    cd pybooru
    sudo python setup.py build
    sudo python setup.py install
```

Example use.
------------------------------------------------------------------------
```python
from pybooru import Pybooru

client = Pybooru('Konachan')

artists = client.artists('ma')

for artist in artists:
    print 'Name: %s' % (artist['name'])
```

Login example.
------------------------------------------------------------------------
```python
from pybooru import Pybooru

client = Pybooru('Konachan', username='your-username', password='your-password')

client.comments_create(post_id=id, comment_body='Comment content')
```

Special Thanks to.
------------------------------------------------------------------------
