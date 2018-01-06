Quick Start Guide
=================

Features
--------

- Support Danbooru API (version: 2.105.0 - 77e06b6).
- Support Moebooru API (version: 1.13.0+update.3).
- Defult site list.
- JSON responses.
- Custom user-agent.

Installation
------------

You can download and install Pybooru from `Pypi <https://pypi.python.org/pypi/Pybooru/>`_

.. code-block:: bash

  pip install --user Pybooru
..

Install from source
-------------------

.. code-block:: bash

  git clone git://github.com/luquedaniel/pybooru.git
  cd pybooru
  pip install --user -r requirements.txt
  sudo python setup.py build
  python setup.py install
..

Example of use with Danbooru
----------------------------

.. code-block:: python

    from pybooru import Danbooru

    client = Danbooru('danbooru')
    artists = client.artist_list('ma')

    for artist in artists:
        print("Name: {0}".format(artist['name']))
..

login (only for functions that **requires login**):

You can pass two parameters to authenticate: "username" and "api_key". You can see your API key in your profile.

Example:

.. code-block:: python

    from pybooru import Danbooru

    client = Danbooru('danbooru', username='your-username', api_key='your-apikey')
    client.comment_create(post_id=id, body='Comment content')
..

Example of use with Moebooru
----------------------------

.. code-block:: python

    from pybooru import Moebooru

    client = Moebooru('konachan')
    artists = client.artist_list(name='ma')

    for artist in artists:
        print("Name: {0}".format(artist['name']))
..

Some functions may require you to authenticate:

- **username**: your site username.
- **password**: your password in plain text.
- **hash_string** (requires only for sites that isn't in default site list): a string to be hashed with your password.

Example using default sites:

.. code-block:: python

    from pybooru import Moebooru

    client = Moebooru('konachan', username='your-username', password='your-password')
    client.comment_create(post_id=id, comment_body='Comment content')
..

Example using not default sites:

.. code-block:: python

    from pybooru import Moebooru

    client = Moebooru('konachan.com', username='your-username', password='your-password',
                      hash_string='So-I-Heard-You-Like-Mupkids-?--{0}--')
    client.comment_create(post_id=id, comment_body='Comment content')
..


See more examples of `Danbooru <https://github.com/LuqueDaniel/pybooru/tree/master/examples/danbooru>`_ and `Moebooru <https://github.com/LuqueDaniel/pybooru/tree/master/examples/moebooru>`_.

Default sites list
------------------

Pybooru has a list of default sites that allow you to use Pybooru without "site_url" argument:

- konachan (`Konachan <http://konachan.com/>`_)
- yandere (`Yande.re <https://yande.re/post>`_)
- danbooru (`Danbooru <http://danbooru.donmai.us/>`_)
- safebooru (`Safebooru <http://safebooru.donmai.us/>`_)
