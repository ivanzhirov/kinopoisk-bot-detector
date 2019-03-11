
import crawler
import pipelines

from selenium import webdriver
# from xvfbwrapper import Xvfb
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def start():
    # cap marvel
    # pipeline = pipelines.Pipeline(
    #     crawler.MoviePageCrawler(movie_id=843859)
    # ).then(
    #     lambda crawl: crawl.fetch()
    # ).then(
    #     lambda html:
    # )

    # with Xvfb() as display:
    #     browser = webdriver.Firefox()
    #     browser.get('http://ya.ru')
    #     print(browser.title)
    #     browser.quit()
    print('hello')
    driver = webdriver.Remote(
        command_executor='http://hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )
    driver.get('http://ya.ru')
    print( driver.title )
    driver.quit()


if __name__ == '__main__':
    start()

