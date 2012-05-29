from pybooru import Pybooru

client = Pybooru(name='konachan')

wiki = client.wiki('date',2,1,'girl')

for msg in wiki:
	print 'Mensaje: %s' % (msg['body']),

#posts = client.posts(2,0,'yuri')

#for post in posts:
#	print 'URL imagen: %s' % (post['file_url'])

#tags = client.tags(100, 0, 'date')

#print tags
#for tag in tags:
#	print "Nombre: %s ----- %i" % (tag['name'], tag['type'])