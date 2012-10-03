from Pybooru import Pybooru

client = Pybooru('Konachan')

posts = client.posts('blue_eyes', 10)

for post in posts:
    print 'URL imagen: %s' % (post['file_url'])
