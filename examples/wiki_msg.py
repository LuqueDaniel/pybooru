from pybooru import Pybooru

client = Pybooru('yandere')

wiki = client.wiki_list('nice', 'date', 2, 1)

for msg in wiki:
    print 'Mensaje: %s' % (msg['body']),
