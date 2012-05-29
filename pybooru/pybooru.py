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
						  'chan-sankaku': 'chan.sankakucomplex.com',
						  'idol-sankaku': 'idol.sankakucomplex.com',
						  '3dbooru': 'behoimi.org',
						  'nekobooru': 'ekobooru.net'}

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
			raise PybooruError('Error in _json_load', self.openURL.getcode())

	def _url_build(self, api_url, params):
			self.url_request = self.baseURL + api_url + params
			self.url_request = self._json_load(self.url_request)
			return self.url_request

	def posts(self, limit=10, page=1, tags=None):
		self.posts_url = '/post/index.json?'
		self.params = 'limit=%i&page=%i' % (limit, page)

		if tags is not None:
			self.params += '&tags=%s' % (tags)
			return self._url_build(self.posts_url, self.params)
		else:
			return self._url_build(self.posts_url, self.params)

	def tags(self, limit=100, page=1, order='name', id_=None, after_id=0, name=None):
		self.tags_url = '/tag/index.json?'

		if id_ is not None:
			self.params = 'id=%i' % (id_)
			return self._url_build(self.tags_url, self.params)
		if name is not None:
			self.params = "name=%s" % (name)
			return self._url_build(self.tags_url, self.params)
		else:
			self.params = "limit=%i&page=%i&order=%s&after_id=%i" % (limit, page, order, after_id)
			return self._url_build(self.tags_url, self.params)

	def artists(self, name=None, id_=None, limit=20, order='name', page=1):
		self.artists_url = '/artist/index.json?'
		self.params = 'limit=%i&page%i&order=%s' % (limit, page, order)

		if name is not None:
			self.params += '&name=%s' % (name)
			return self._url_build(self.artists_url, self.params)
		elif id_ is not None:
			self.params = 'id=%i' % (id_)
			return self._url_build(self.artists_url, self.params)
		else:
			return self._url_build(self.artists_url, self.params)

	def comments(self, id_=None):
		self.omments_url = 'comment/show.json?'

		if id_ is not None:
			self.params = 'id=%i' % (id_)
		else:
			print PybooruError('id_ attribute is empty')


class PybooruError(Exception):
	def __init__(self, err_msg, err_code=None):
		self.err_msg = err_msg

		if err_code is not None:
			if err_code == 200:
				self.err_msg = '%s - ERROR CODE:%i - Request was successful' % (self.err_msg, err_code)
			elif err_code == 403:
				self.err_msg = '%s - ERROR CODE:%i - Access denied' % (self.err_msg, err_code)
			elif err_code == 404:
				self.err_msg = '%s - ERROR CODE:%i - Not found' % (self.err_msg, err_code)
			elif err_code == 420:
				self.err_msg = '%s - ERROR CODE:%i - Record could not be saved' % (self.err_msg, err_code)
			elif err_code == 421:
				self.err_msg = '%s - ERROR CODE:%i - User is throttled, try again later' % (self.err_msg, err_code)
			elif err_code == 422:
				self.err_msg = '%s - ERROR CODE:%i - The resource is locked and cannot be modified' % (self.err_msg, err_code)
			elif err_code == 423:
				self.err_msg = '%s - ERROR CODE:%i - Resource already exists' % (self.err_msg, err_code)
			elif err_code == 424:
				self.err_msg = '%s - ERROR CODE:%i - The given parameters were invalid' % (self.err_msg, err_code)
			elif err_code == 500:
				self.err_msg = '%s - ERROR CODE:%i - Some unknown error occurred on the server' % (self.err_msg, err_code)
			elif err_code == 503:
				self.err_msg = '%s - ERROR CODE:%i - Server cannot currently handle the request, try again later' % (self.err_msg, err_code)

	def __str__(self):
		return repr(self.err_msg)

if __name__ == '__main__':
	print PybooruError('import this module into your project to use')