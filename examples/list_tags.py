from pybooru import Pybooru

client = pybooru('Danbooru')

tags = client.tags(None, None, 100, 0, 'date')

for tag in tags:
	print "Nombre: %s ----- %i" % (tag['name'], tag['type'])