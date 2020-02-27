from pybooru.tests.helpers import test_all_sites
from unittest2 import TestCase


class TestConfig(TestCase):
    @test_all_sites
    def test_reqired_entries(self, site, config):
        self.assertIn('url', config)
