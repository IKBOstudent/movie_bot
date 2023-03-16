import json
from os.path import splitext

from requests import Response
from requests_cache import CachedSession, FileCache, FileDict


class JSONFileCache(FileCache):
    def __init__(self, cache_name, **kwargs):
        super().__init__(cache_name, **kwargs)
        self.responses = JSONFileDict(cache_name, **kwargs)


class JSONFileDict(FileDict):
    def __setitem__(self, key: str, value: Response):
        super().__setitem__(key, value)
        response_path = splitext(self._path(key))[0]
        json_path = f'{response_path}_content.json'

        with self._try_io(ignore_errors=True):
            content = json.dumps(value.json(), indent=2)
            with open(json_path, 'w') as f:
                f.write(content)
