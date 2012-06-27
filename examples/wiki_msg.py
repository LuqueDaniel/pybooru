from pybooru import Pybooru

client = Pybooru('yandere')

wiki = client.wiki('nice', 'date', 2, 1)

for msg in wiki:
    print 'Mensaje: %s' % (msg['body']),
