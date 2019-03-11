import re

import exceptions

import selenium.common.exceptions


class MapperXpathField:
    def __init__(self, xpath):
        self.xpath = xpath
        self.val = None

    def get(self, body):
        try:
            return body.find_element_by_xpath(self.xpath).text
        except selenium.common.exceptions.NoSuchElementException:
            raise exceptions.ParsingException()


class TotalMovieCountField(MapperXpathField):
    def get(self, body):
        val = super().get(body)

        found = re.search(r'История оценок \((.*?)\)', val)
        if not found:
            raise exceptions.ParsingException()

        return found.group(1)


class UserIDField(MapperXpathField):
    def get(self,  body):
        try:
            link = body.find_element_by_xpath(
                self.xpath).get_attribute("href")
        except selenium.common.exceptions.NoSuchElementException:
            raise exceptions.ParsingException()

        found = re.search(r'/user/(.*?)/', link)
        if not found:
            raise exceptions.ParsingException()

        return found.group(1)
