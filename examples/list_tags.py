from pybooru import Pybooru

client = Pybooru('Konachan')

tags = client.tags_list(None, None, 100, 0, 'date')

for tag in tags:
    print "Nombre: %s ----- %i" % (tag['name'], tag['type'])
