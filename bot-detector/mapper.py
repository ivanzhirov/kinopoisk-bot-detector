import re

import exceptions

import selenium.common.exceptions


class MapperXpathField:
    def __init__(self, select):
        self.select = select
        self.val = None

    def get(self, body):
        try:
            val = body.select(self.select)[0].string
            return val and val.strip()
        except Exception:
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
            link = body.select(self.select)[0]["href"]
        except selenium.common.exceptions.NoSuchElementException:
            raise exceptions.ParsingException()

        found = re.search(r'/user/(.*?)/', link)
        if not found:
            raise exceptions.ParsingException()

        return found.group(1)
