#encoding: utf-8

import urllib
import simplejson

__author__ = 'Daniel Luque <danielluque14@gmail.com>'
__version__ = '1.0.0'

class Danbooru(object):
	def __init__(self, name=None, siteURL=None):
		self.baseURL = ''

		if siteURL is not None:
			self.siteURL = str(siteURL).lower()
			self.baseURL = self.siteURL
		elif name is not None:
			self.name = str(name).lower()
			self._site_name(self.name)
		else:
			print "siteURL or name invalid"

	def _site_name(self,name):
		self.site_list = {'konachan': 'http://konachan.com',
						  'danbooru': 'http://danbooru.donmai.us',
						  'yandere': 'https://yande.re'}

		if name in self.site_list.keys():
			self.baseURL = self.site_list[name]
		else:
			print "Site name is not valid"

	def _json_load(self, url):
		try:
			self.openURL = urllib.urlopen(url)
			self.request = self.openURL.read()
			self.response = simplejson.loads(self.request)
			return self.response
		except:
			self._Errors(self.openURL.getcode())

	def _Errors(self, err_code):
		if err_code == 200: print 'ERROR:%i - Request was successful' % (err_code)
		elif err_code == 403: print 'ERROR:%i - Access denied' % (err_code)
		elif err_code == 404: print 'ERROR:%i - Not found' % (err_code)
		elif err_code == 420: print 'ERROR:%i - Record could not be saved' % (err_code)
		elif err_code == 421: print 'ERROR:%i - User is throttled, try again later' % (err_code)
		elif err_code == 422: print 'ERROR:%i - The resource is locked and cannot be modified' % (err_code)
		elif err_code == 423: print 'ERROR:%i - Resource already exists' % (err_code)
		elif err_code == 424: print 'ERROR:%i - The given parameters were invalid' % (err_code)
		elif err_code == 500: print 'ERROR:%i - Some unknown error occurred on the server' % (err_code)
		elif err_code == 503: print 'ERROR:%i - Server cannot currently handle the request, try again later' % (err_code)

	def posts(self, limit=10, page=1, tags=None):
		self.posts_url = '/post/index.json?'
		self.params = 'limit=%i&page=%i' % (limit, page)

		if tags is not None:
			self.params += '&tags=%s' % (tags)
			self.url_request = self.baseURL + self.posts_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request
		else:
			self.url_request = self.baseURL + self.posts_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request

	def tags(self, limit=100, page=1, order='name', id_=None, after_id=0, name=None):
		self.tags_url = '/tag/index.json?'

		if id_ is not None:
			self.params = 'id=%i' % (id_)
			self.url_request = self.baseURL + self.tags_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request

		if name is not None:
			self.params = "name=%s" % (name)
			self.url_request = self.baseURL + self.tags_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request

		else:
			self.params = "limit=%i&page=%i&order=%s&after_id=%i" % (limit, page, order, after_id)
			self.url_request = self.baseURL + self.tags_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request

	def artists(self, name=None, id_=None, limit=20, order='name', page=1):
		self.artists_url = '/artist/index.json?'
		self.params = 'limit=%i&page%i&order=%s' % (limit, page, order)

		if name is not None:
			self.params += '&name=%s' % (name)
			self.url_request = self.baseURL + self.artists_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request
		elif id_ is not None:
			self.params = 'id=%i' % (id_)
			self.url_request = self.baseURL + self.artists_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request
		else:
			self.url_request = self.baseURL + self.artists_url + self.params
			self.url_request = self._json_load(self.url_request)
			return self.url_request
	def comments (self, id_=None):
		self.omments_url = 'comment/show.json?'

	def probando(self):
		print self.baseURL


client = Danbooru(name='Konachan')
posts = client.posts(2,0)

for post in posts:
	print 'URL imagen: %s' % (post['file_url'])

#tags = client.tags(100, 0, 'date')

#print tags
#for tag in tags:
#	print "Nombre: %s ----- %i" % (tag['name'], tag['type'])