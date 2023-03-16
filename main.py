import json


import requests
from dotenv import load_dotenv

from handlers import bot_service
from utils import CachedSession, JSONFileCache

load_dotenv()


class FilmFetch:
    def __init__(self, url, headers, params):
        self.url = url
        self.headers = headers
        self.params = params

    def cached_request(self):
        custom_backend = JSONFileCache('cached_requests', serializer='json')
        session = CachedSession(backend=custom_backend)
        data = session.get(self.url, headers=self.headers, params=self.params).json()
        return data

    def standard_request(self):
        data = requests.get(self.url, headers=self.headers, params=self.params).json()
        return data


if __name__ == "__main__":
    # url = 'https://api.kinopoisk.dev/v1/movie'
    # headers = {"X-API-KEY": os.API_KEY}
    # params = {
    #     'id': 335
    # }
    # MementoFetch = FilmFetch(url, headers, params)
    # print(MementoFetch.cached_request())

    print("bot running")
    bot_service.infinity_polling()







