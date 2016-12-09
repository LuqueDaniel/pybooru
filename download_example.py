from __future__ import unicode_literals
from pybooru import Danbooru
from random import randint
import urllib.request

x = []

def download(tags, pages):
	try:
		randomint = randint(1000, 10000000)
		randompage = randint(1, int(pages))
		client = Danbooru('danbooru', username='your_username', api_key='your_api_key')
		if len(x) == 0: #Checks if the array is empty of links
			posts = client.post_list(tags=str(tags), page=str(randompage), limit=200)
			for post in posts:
				fileurl = 'http://danbooru.donmai.us' + post['file_url']
				x.append(fileurl)
		else:
			pass
		try:
			urllib.request.urlretrieve(x[1], "tmp/danbooru_" + str(randomint) + ".jpg")
			x.pop(0)
		except Exception as e:
			print(e)
	except:
		download(tags, pages)

def main():
	download(tags='rating:s', pages='2000') #Gold account limit
	
main()
