import re
import typing

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import contracts
import exceptions


def fetch_user(user_id):
    browser = UserPageCrawler(user_id=user_id)
    user = browser.fetch()
    browser.quit()
    return user


class PageCrawler(webdriver.Remote):
    url_format: str = None

    def __init__(self, **kwargs):
        super().__init__(
            command_executor='http://hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.item = None
        self.kwargs = kwargs

    def fetch(self) -> typing.Union[typing.Any]:
        url = self.url_format.format(**self.kwargs)
        self.get(f'http://kinopoisk.ru{url}')


class MoviePageCrawler(PageCrawler):
    url_format = '/film/{movie_id}/'


class UserPageCrawler(PageCrawler):
    url_format = '/user/{user_id}/'

    def fetch(self) -> contracts.UserContract:
        super().fetch()
        return contracts.UserContract(body=self)


class MovieVotePageCrawler(PageCrawler):
    url_format = '/film/{movie_id}/votes/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wait = WebDriverWait(self, 10)

    def get_votes(self, max_count=None, prefetch_rules=None, user_rules=None):
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "rating_list")))

        # get number of elements
        rating_items = self.find_elements_by_class_name('rating_item')

        # wip
        ret = []
        for index, item in enumerate(rating_items):
            if max_count and index >= max_count:
                break

            ret.append(contracts.RatingItem(body=item).to_dict())

        return ret

