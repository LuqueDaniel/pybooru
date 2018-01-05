from __future__ import unicode_literals
from pybooru import Danbooru
from random import randint
import urllib.request


x = []  # link storage


def download(tags, pages):
    try:
        client = Danbooru('danbooru', username='your_username', api_key='your_api_key')

        # Collect links
        while len(x) is not 200:  # Checks if the list is full
            randompage = randint(1, pages)
            posts = client.post_list(tags=tags, page=randompage, limit=200)
            for post in posts:
                try:
                    fileurl = 'https://danbooru.donmai.us' + post['file_url']
                except:
                    fileurl = 'https://danbooru.donmai.us' + post['source']
                x.append(fileurl)

        # Download images
        for url in x:
            try:
                randomint = randint(1000, 10000000)
                urllib.request.urlretrieve(url, "tmp/danbooru_/{0}.jpg".format(randomint))
            except:
                continue
    except Exception as e:
        raise e


def main():
    # pages: 2000 Gold account limit. Basic Users should have 1000
    download(tags='rating:s', pages=1000)


main()
