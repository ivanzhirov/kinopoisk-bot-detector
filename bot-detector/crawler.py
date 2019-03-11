import bs4
import requests


class PageCrawler:
    url_format = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def fetch(self):
        url = self.url_format.format(**self.kwargs)
        response = requests.get(f'http://kinopoisk.ru{url}')
        return bs4.BeautifulSoup(response.content)


class MoviePageCrawler(PageCrawler):
    url_format = '/film/{movie_id}/'


class UserPageCrawler(PageCrawler):
    url_format = '/user/{user_id}/'
