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
    print('user1')
    user = browser.fetch()
    print(user)
    # browser.quit()
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait = WebDriverWait(self, 10)
        self.contract = contracts.MovieContract(body=self)

    def get_current_votes_length(self) -> int:
        return len(self.find_elements_by_class_name('rating_item'))

    def get_votes(self, max_count=None, prefetch_rules=None, user_rules=None):
        print(f'Total votes: {self.contract.total_votes}')

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "rating_list")))

        if max_count is None:
            max_count = self.contract.total_votes

        # get number of elements
        current_items = 0

        print("Started to lazy load votes")

        while current_items <= max_count:
            current_items = self.get_current_votes_length()
            print(f'Items {current_items}')
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            self.wait.until(
                lambda driver: current_items != self.get_current_votes_length())

            current_items = self.get_current_votes_length()

        # self.quit()
        print('Going to fetch users')

        ret = []
        for item in filter(lambda y: all(rule(y) for rule in prefetch_rules), map(
            lambda x: contracts.RatingItem(body=x).to_dict(),
            self.find_elements_by_class_name('rating_item')
        )):
           print(item)
           user_browser = UserPageCrawler(user_id=item['user_id'])
           print('here')
           user = user_browser.fetch()
           print(user)
           if all(rule(user) for rule in user_rules):
               ret.append(user)

        return ret

