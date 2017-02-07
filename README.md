# Pybooru - Package for Danbooru/Moebooru API.
[![PyPI](https://img.shields.io/pypi/v/Pybooru.svg?style=flat-square)](https://pypi.python.org/pypi/Pybooru/)
[![PyPI](https://img.shields.io/pypi/status/Pybooru.svg?style=flat-square)](https://pypi.python.org/pypi/Pybooru/)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/LuqueDaniel/pybooru/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/pybooru/badge/?version=stable)](http://pybooru.readthedocs.io/en/stable/?badge=stable)

**Pybooru** is a Python package to access to the API of Danbooru/Moebooru based sites.

- Version: **4.1.0**
- Licensed under: **MIT License**

## Dependencies.
- Python: >= 2.7 or Python: >= 3.3
- [requests](http://docs.python-requests.org/en/latest/)

## Installation
### from Python Package Index (Pypi)
[Pybooru on Pypi.](https://pypi.python.org/pypi/Pybooru/)

```bash
pip install --user Pybooru
```

### Manual installation
```bash
git clone git://github.com/luquedaniel/pybooru.git
cd pybooru
pip install --user -r requirements.txt
sudo python setup.py build
python setup.py install
```

## Examples of use
See [More examples](https://github.com/LuqueDaniel/pybooru/tree/master/examples).

### Danbooru
```python
from pybooru import Danbooru

client = Danbooru('danbooru')
artists = client.artist_list('ma')

for artist in artists:
    print("Name: {0}".format(artist['name']))
```

#### Login example
```python
from pybooru import Danbooru

client = Danbooru('danbooru', username='your-username', api_key='your-apikey')
client.comment_create(post_id=id, body='Comment content')
```

### Moebooru
```python
from pybooru import Moebooru

client = Moebooru('konachan')
artists = client.artist_list(name='neko')

for artist in artists:
    print("Name: {0}".format(artist['name']))
```

#### Login example
##### Default sites
```python
from pybooru import Moebooru

client = Moebooru('konachan', username='your-username', password='your-password')
client.comment_create(post_id=id, comment_body='Comment content')
```

##### Not default sites
```python
from pybooru import Moebooru

client = Moebooru('konachan.com', username='your-username', password='your-password',
                  hash_string='So-I-Heard-You-Like-Mupkids-?--{0}--')
client.comment_create(post_id=id, comment_body='Comment content')
```

## Documentation
You can consult the documentation on **[Read the Docs](http://pybooru.readthedocs.io/en/stable/)**

## Status
| Platform       | Master         | Develop |
| :------------- | :------------- | :------- |
| [Linux & OSX (Travis CI)](https://travis-ci.org/LuqueDaniel/pybooru) | [![Travis CI](https://travis-ci.org/LuqueDaniel/pybooru.svg?branch=master)](https://travis-ci.org/LuqueDaniel/pybooru) | [![Travis CI](https://travis-ci.org/LuqueDaniel/pybooru.svg?branch=develop)](https://travis-ci.org/LuqueDaniel/pybooru) |
| [Windows (AppVeyor)](https://ci.appveyor.com/project/LuqueDaniel/pybooru) | [![AppVeyor](https://img.shields.io/appveyor/ci/luquedaniel/pybooru.svg)](https://ci.appveyor.com/project/LuqueDaniel/pybooru) | [![AppVeyor](https://img.shields.io/appveyor/ci/luquedaniel/pybooru/develop.svg)](https://ci.appveyor.com/project/LuqueDaniel/pybooru) |

## License
- **[See MIT License](https://github.com/LuqueDaniel/pybooru/blob/master/LICENSE)**
