from pybooru import Pybooru

client = Pybooru(name='Konachan')

notes = client.notes()

print notes

#wiki = client.wiki('yuri', 'date', 2, 1)

#for msg in wiki:
#	print 'Mensaje: %s' % (msg['body']),

#posts = client.posts('yuri', 2, 0)

#for post in posts:
#	print 'URL imagen: %s' % (post['file_url'])

#tags = client.tags(None, None, 100, 0, 'date')

#print tags
#for tag in tags:
#	print "Nombre: %s ----- %i" % (tag['name'], tag['type'])