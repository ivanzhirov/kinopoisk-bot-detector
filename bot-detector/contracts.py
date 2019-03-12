import bs4
import selenium.webdriver.remote.webelement

import mapper


class Contracts:
    def __init__(self, driver):
        if isinstance(driver, selenium.webdriver.remote.webelement.WebElement):
            html = driver.get_attribute('innerHTML')
        else:
            html = driver.page_source

        self.body = bs4.BeautifulSoup(html, features="html.parser")

    def __getattribute__(self, item):
        val = object.__getattribute__(self, item)
        if issubclass(
            val.__class__,
            mapper.MapperXpathField
        ):
            return val.get(body=self.body)
        return val

    def to_dict(self):
        return {
            k: getattr(self, k)
            for k in dir(self)
            if issubclass(
                object.__getattribute__(self, k).__class__,
                mapper.MapperXpathField
            )
        }


class MovieContract(Contracts):
    total_votes: int = mapper.IntMapperXPathField(
        r=r'История оценок \((.*?)\)',
        select='#block_left > div > table > tbody > tr:nth-child(3) > td > '
               'table:nth-child(1) > tbody > tr:nth-child(1) > td > table'
               ' > tbody > tr > td > h2')


class RatingItem(Contracts):
    user_id: int = mapper.IntMapperXPathField(
        r=r'/user/(.*?)/',
        attr='href',
        select='td.comm-user > div > p > a')

    vote: int = mapper.IntMapperXPathField(
        select='td.comm-title > div > table > tbody > tr > td')


class UserContract(Contracts):
    movie_number: int = mapper.IntMapperXPathField(
        select='#profileInfoWrap > div.profileInfoWrapBottom > div > '
               'ul > li:nth-child(1) > a > b')

    user_id: int = mapper.IntMapperXPathField(
        r=r'/mykp/sendmessage/(.*?)/',
        attr='href',
        select='#profileInfoWrap > div.profileInfoWrapLeft > a')
