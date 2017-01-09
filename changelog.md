# Pybooru - Changelog

## Pybooru 4.0.1 - (2016/12/09)
- Fix problems with Pypi

## Pybooru 4.0.0 - (2016/12/09)
- Added support to Danbooru
- Now Danbooru and Moebooru are two separed classes
- Pybooru has been refactored
- Moebooru (only): added support for API versioning
- Added PybooruAPIError exception
- Added **last_call** attribute to Danbooru and Moebooru to store last request information
- Examples has been updated
- Added **[documentation](http://pybooru.readthedocs.io/en/stable/)** to Pybooru (with Sphinx)
- Added some tools for Pybooru (tools folder)
- Refactored setup.py
- End of Python 3.2.x support
- Fixed parameter comparison (python 2.X only)
- In this version there's a nice amount of improvements

## Pybooru 3.0.1 - (2015/01/13)
- Minors changes

## Pybooru 3.0 - (2014/12/06)
- In this version there's a nice amount of code improvements
- Added compatibility with Python 3
- Pybooru now use requests
- Replace `"%s" % (foo)` for `"{0}".format(foo)`
- Improvement code style
- Added Travis CI to the project

## Pybooru 2.1.1 - (2013/12/26)
- Improve documentation style

## Pybooru 2.1 - (2013/10/14)
- Added login suppport for any Moebooru based site
- Fixed a bug: #c4b3435
- Added new information to setup.py
- Small changes
