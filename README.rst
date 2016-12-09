Pybooru - Package for Danbooru/Moebooru API.
============================================
.. image:: https://img.shields.io/pypi/v/Pybooru.svg?style=flat-square
.. image:: https://img.shields.io/pypi/status/Pybooru.svg?style=flat-square
.. image:: https://img.shields.io/pypi/l/Pybooru.svg?style=flat-square
    :target: https://raw.githubusercontent.com/LuqueDaniel/pybooru/master/LICENSE
.. image:: https://img.shields.io/pypi/wheel/Pybooru.svg?style=flat-square
.. image:: https://img.shields.io/pypi/format/Pybooru.svg?style=flat-square


Examples of use
---------------
.. code-block:: python

   from pybooru import Danbooru

   client = Danbooru('danbooru')
   artists = client.artist_list('ma')

   for artist in artists:
        print("Name: {0}".format(artist['name']))

See more examples of `Danbooru <https://github.com/LuqueDaniel/pybooru/tree/develop/examples/danbooru>`_ and `Moebooru <https://github.com/LuqueDaniel/pybooru/tree/develop/examples/moebooru>`_.

Documentation
-------------
You can consult the `documentation <http://pybooru.readthedocs.io/en/stable/>`_

Changelog
---------
- https://github.com/LuqueDaniel/pybooru/blob/master/changelog.md

Github repository
-----------------
- https://github.com/LuqueDaniel/pybooru

More information
----------------
- https://github.com/LuqueDaniel/pybooru/blob/master/README.markdown
