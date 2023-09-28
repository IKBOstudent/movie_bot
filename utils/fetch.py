    # pylint: disable-all

import json
import os

import requests
from requests_cache import CachedSession, FileCache, FileDict


class JSONFileCache(FileCache):

    def __init__(self, cache_name, **kwargs):
        super().__init__(cache_name, **kwargs)
        self.responses = JSONFileDict(cache_name, **kwargs)


class JSONFileDict(FileDict):
    def __setitem__(self, key: str, value: requests.Response):
        super().__setitem__(key, value)
        response_path = os.path.splitext(self._path(key))[0]
        json_path = f'{response_path}_content.json'

        with self._try_io(ignore_errors=True):
            content = json.dumps(value.json(), indent=2)
            with open(json_path, 'w') as f:
                f.write(content)


class FilmFetch:
    """Film fetch options"""

    def __init__(self, url, params):
        self.url = url
        self.headers = {"X-API-KEY": "9RM0E02-E2BMGJ0-HZ1YJSS-43SH5RX"}
        self.params = params

    def cached_request(self):
        """
        Request with CachedSession.
            Response not found in cache ->
            sends HTTP request. Then puts response in cache.

            Response found in cache -> gets data from cache.
        """

        custom_backend = JSONFileCache('cached_requests', serializer='json')
        session = CachedSession(backend=custom_backend)

        data = session.get(self.url, headers=self.headers, params=self.params).json()
        return data

    def standard_request(self):
        """Standard HTTP request"""

        data = requests.get(self.url, headers=self.headers, params=self.params).json()
        return data
