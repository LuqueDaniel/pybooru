#encoding: utf-8

import urllib
import simplejson

__author__ = 'Daniel Luque <danielluque14@gmail.com>'
__version__ = '1.0.0'


class Pybooru(object):
	def __init__(self, name=None, siteURL=None):
		self.baseURL = ''

		if siteURL is not None:
			self.siteURL = str(siteURL).lower()
			self.baseURL = siteURL
		elif name is not None:
			self.name = str(name).lower()
			self._site_name(self.name)
		else:
			print PybooruError('siteURL or name invalid')

	def _site_name(self,name):
		self.site_list = {'konachan': 'http://konachan.com',
						  'danbooru': 'http://danbooru.donmai.us',
						  'yandere': 'https://yande.re',
						  'chan-sankaku': 'htpp://chan.sankakucomplex.com',
						  'idol-sankaku': 'http://idol.sankakucomplex.com',
						  '3dbooru': 'http://behoimi.org',
						  'nekobooru': 'http://nekobooru.net'}

		if name in self.site_list.keys():
			self.baseURL = self.site_list[name]
		else:
			print PybooruError('Site name is not valid')

	def _json_load(self, url):
		try:
			self.openURL = urllib.urlopen(url)
			self.request = self.openURL.read()
			self.response = simplejson.loads(self.request)
			return self.response
		except:
			raise PybooruError('Error in _json_load', self.openURL.getcode(), url)

	def _url_build(self, api_url, params=None):
		if params is not None:
			self.url_request = self.baseURL + api_url + params
			self.url_request = self._json_load(self.url_request)
			return self.url_request
		else:
			self.url_request = self.baseURL + api_url
			self.url_request = self._json_load(self.url_request)
			return self.url_request

	def posts(self, tags=None, limit=10, page=1):
		self.posts_url = '/post/index.json?'
		self.params = 'limit=%i&page=%i' % (limit, page)

		if tags is not None:
			self.tags = str(tags)
			self.params += '&tags=%s' % (tags)
			return self._url_build(self.posts_url, self.params)
		else:
			return self._url_build(self.posts_url, self.params)

	def tags(self, name=None, id_=None, limit=100, page=1, order='name', after_id=0):
		self.tags_url = '/tag/index.json?'

		if id_ is not None:
			self.params = 'id=%i' % (id_)
			return self._url_build(self.tags_url, self.params)
		if name is not None:
			self.name = str(name)
			self.params = "name=%s" % (self.name)
			return self._url_build(self.tags_url, self.params)
		else:
			self.params = "limit=%i&page=%i&order=%s&after_id=%i" % (limit, page, order, after_id)
			return self._url_build(self.tags_url, self.params)

	def artists(self, name=None, id_=None, limit=20, order='name', page=1):
		self.artists_url = '/artist/index.json?'
		self.params = 'limit=%i&page%i&order=%s' % (limit, page, order)

		if name is not None:
			self.name = str(name)
			self.params += '&name=%s' % (self.name)
			return self._url_build(self.artists_url, self.params)
		elif id_ is not None:
			self.params = 'id=%i' % (id_)
			return self._url_build(self.artists_url, self.params)
		else:
			return self._url_build(self.artists_url, self.params)

	def comments(self, id_=None):
		self.comments_url = '/comment/show.json?'

		if id_ is not None:
			self.params = 'id=%i' % (id_)
			return self._url_build(self.comments_url, self.params)
		else:
			print PybooruError('id_ attribute is empty')

	def wiki(self, query=None, order='title', limit=20, page=1):
		self.wiki_url = '/wiki/index.json?'
		self.params = 'order=%s&limit=%i&page=%i' % (order, limit, page)

		if query is not None:
			self.query = str(query)
			self.params += '&query=%s' % (self.query)
			return self._url_build(self.wiki_url, self.params)
		else:
			return self._url_build(self.wiki_url, self.params)

	def notes(self, id_=None):
		self.notes_url = '/note/index.json?'

		if id_ is not None:
			self.params = 'post_id=%i' % (id_)
			return self._url_build(self.notes_url, self.params)
		else:
			return self._url_build(self.notes_url)

	def search_notes(self, query=None):
		self.search_notes_url = '/note/search.json?'

		if query is not None:
			self.query = str(query)
			self.params = 'query=%s' % (self.query)
			return self._url_build(self.search_notes_url, self.params)
		else:
			print PybooruError('query attribute is empty')

	def history_notes(self, post_id=None, id_=None, limit=10, page=1):
		self.history_notes_url = '/note/history.json?'

		if post_id is not None:
			self.params = 'post_id=%i' % (post_id)
			return self._url_build(self.history_notes_url, self.params)
		elif id_ is not None:
			self.params = 'id=%i' % (post_id)
			return self._url_build(self.history_notes_url, self.params)
		else:
			self.params = 'limit=%i&page=%i' % (limit, page)
			return self._url_build(self.history_notes_url, self.params)

	def users(self, name=None, id_=None):
		self.users_url = '/user/index.json?'

		if name is not None:
			self.name = str(name)
			self.params = 'name=%s' % (self.name)
			return self._url_build(self.users_url, self.params)
		elif id_ is not None:
			self.params = 'id=%i' % (self.id_)
			return self._url_build(self.users_url, self.params)
		else:
			return self._url_build(self.users_url)

	def forum(self, id_=None):
		self.forum_url = '/forum/index.json?'

		if id_ is not None:
			self.params = 'parent_id%i' % (id_)
			return self._url_build(self.forum_url, self.params)
		else:
			return self._url_build(sel.forum_url)


class PybooruError(Exception):
	def __init__(self, err_msg, err_code=None, url=None):
		self.err_msg = err_msg

		if err_code is not None and url is not None:
			if err_code == 200:
				self.err_msg = '%s - ERROR CODE:%i - Request was successful - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 403:
				self.err_msg = '%s - ERROR CODE:%i - Access denied - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 404:
				self.err_msg = '%s - ERROR CODE:%i - Not found - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 420:
				self.err_msg = '%s - ERROR CODE:%i - Record could not be saved - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 421:
				self.err_msg = '%s - ERROR CODE:%i - User is throttled, try again later - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 422:
				self.err_msg = '%s - ERROR CODE:%i - The resource is locked and cannot be modified - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 423:
				self.err_msg = '%s - ERROR CODE:%i - Resource already exists - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 424:
				self.err_msg = '%s - ERROR CODE:%i - The given parameters were invalid - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 500:
				self.err_msg = '%s - ERROR CODE:%i - Some unknown error occurred on the server - URL: %s' % (self.err_msg, err_code, url)
			elif err_code == 503:
				self.err_msg = '%s - ERROR CODE:%i - Server cannot currently handle the request, try again later - URL: %s' % (self.err_msg, err_code, url)

	def __str__(self):
		return repr(self.err_msg)


if __name__ == '__main__':
	print PybooruError('import this module into your project to use')