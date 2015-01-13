Pybooru - Library for Danbooru/Moebooru API.
============================================
.. image:: https://travis-ci.org/LuqueDaniel/pybooru.svg?branch=master
    :target: https://travis-ci.org/LuqueDaniel/pybooru

Pybooru is a Python library to access API of Danbooru/Moebooru based sites.

Licensed under: **MIT License**.

Examples of use
---------------
.. code-block:: python

   from pybooru import Pybooru

   client = Pybooru('Konachan')

   artists = client.artists('ma')

   for artist in artists:
        print("Name: {0}".format(artist['name']))
   ..

See more examples: https://github.com/LuqueDaniel/pybooru/tree/develop/examples

Changelog
---------
- https://github.com/LuqueDaniel/pybooru/blob/master/changelog.md

Github repository
-----------------
- https://github.com/LuqueDaniel/pybooru

More information
----------------
- https://github.com/LuqueDaniel/pybooru/blob/master/README.markdown
