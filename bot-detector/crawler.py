import typing
import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import contracts
import concurrent.futures


def fetch_user(user_data):
    print('Processing user ', user_data)
    browser = UserPageCrawler(user_id=user_data['user_id'])
    user = browser.fetch().to_dict()
    browser.quit()
    return user


class PageCrawler(webdriver.Remote):
    url_format: str = None

    def __init__(self, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_extension("proxy.zip")

        capabilities = options.to_capabilities()

        super().__init__(
            command_executor='http://hub:4444/wd/hub',
            desired_capabilities=capabilities)
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
        return contracts.UserContract(driver=self)


class MovieVotePageCrawler(PageCrawler):
    url_format = '/film/{movie_id}/votes/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait = WebDriverWait(self, 10)
        self.contract = None

    def fetch(self):
        super().fetch()
        self.contract = contracts.MovieContract(driver=self)

    def get_current_votes_length(self) -> int:
        return len(self.find_elements_by_class_name('rating_item'))

    def get_votes(self, max_count=None, prefetch_rules=None, user_rules=None):
        self.fetch()

        print(f'Total votes: {self.contract.total_votes}')

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "rating_list")))

        if max_count is None:
            max_count = self.contract.total_votes

        # get number of elements
        current_items = 0

        print("Started to lazy load votes")

        # fixme: bug with extra offset
        while current_items <= max_count:
            current_items = self.get_current_votes_length()
            print(f'Items {current_items}')
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # fixme: check waiting
            self.wait.until(
                lambda _: current_items != self.get_current_votes_length())

            current_items = self.get_current_votes_length()

        print('Going to fetch users')
        print("Total users to process: ", self.get_current_votes_length())

        data = filter(
            lambda y: all(rule(y) for rule in prefetch_rules),
            map(
              lambda x: contracts.RatingItem(driver=x).to_dict(),
              self.find_elements_by_class_name('rating_item')
            )
        )

        print('Going to process users')

        user_ids = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            gen = executor.map(fetch_user, data)
            for user_page in gen:
                if all(rule(user_page) for rule in user_rules):
                    user_ids.append(user_page)

        return user_ids
