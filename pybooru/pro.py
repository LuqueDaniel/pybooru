from pybooru import Pybooru

client = Pybooru(name='Konachan')

posts = client.posts(2,0,'yuri')

for post in posts:
	print 'URL imagen: %s' % (post['file_url'])

#tags = client.tags(100, 0, 'date')

#print tags
#for tag in tags:
#	print "Nombre: %s ----- %i" % (tag['name'], tag['type'])