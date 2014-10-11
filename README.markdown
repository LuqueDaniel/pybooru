Pybooru - Library for Danbooru API.
========================================================================
Pybooru is a library for Python for access to API Danbooru / Moebooru based sites.

Version: **2.5.0-develop**<br />
Licensed under: **MIT License**

Dependencies.
-------------
- Python: >= 2.6
- [Simplejson](https://pypi.python.org/pypi/simplejson/) (Optional).

Installation.
-------------
**from Python Package Index (Pypi):**<br />
Pypi - Python Package Index:
[Pybooru on Pypi](https://pypi.python.org/pypi/Pybooru/).

```bash
sudo pip install Pybooru
```
or
```bash
sudo easy_install Pybooru
```

**Manual installation:**
```bash
git clone git://github.com/luquedaniel/pybooru.git
cd pybooru
sudo python setup.py build
sudo python setup.py install
```

Example of use.
---------------
```python
from pybooru import Pybooru

client = Pybooru('Konachan')

artists = client.artists('ma')

for artist in artists:
    print 'Name: %s' % (artist['name'])
```

**Login example:**<br />
Default sites:
```python
from pybooru import Pybooru

client = Pybooru('Konachan', username='your-username', password='your-password')

client.comments_create(post_id=id, comment_body='Comment content')
```

Other sites:
```python
from pybooru import Pybooru

client = Pybooru('konachan.com', username='your-username', password='your-password', hashString='So-I-Heard-You-Like-Mupkids-?--%s--')

client.comments_create(post_id=id, comment_body='Comment content')
```

[More examples.](https://github.com/LuqueDaniel/pybooru/tree/master/examples)

CI Report
---------
- https://travis-ci.org/LuqueDaniel/pybooru

License.
--------
- **[MIT License](https://github.com/LuqueDaniel/pybooru/blob/master/LICENSE)**