from functools import wraps
from pybooru.resources import SITE_LIST


def test_all_sites(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        for site_name, config in SITE_LIST.items():
            with self.subTest(site_name=site_name, config=config):
                func(self, site_name, config, *args, **kwargs)
    return wrapper
