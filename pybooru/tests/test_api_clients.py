from pybooru import Danbooru
from pybooru import Moebooru
from pybooru.tests.helpers import test_all_sites
from unittest2 import TestCase


class TestApiClients(TestCase):
    client_mapping = {
        'konachan': Moebooru,
        'yandere': Moebooru,
        'danbooru': Danbooru,
        'safebooru': Danbooru,
    }


    @test_all_sites
    def test_site_is_up(self, site, config):
        client = self.client_mapping[site](site)
        client.tag_list()
        # Close session to prevent warning message from requests module
        # https://github.com/psf/requests/issues/3912
        client.client.close()
        self.assertEqual(client.last_call.get('status_code'), 200)
