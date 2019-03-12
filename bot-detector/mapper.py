import re
import exceptions


class MapperXpathField:
    def __init__(self, select, r=None, attr=None):
        self.select = select
        self.val = None
        self.r = r
        self.attr = attr

    def extracted_attr(self, el):
        if self.attr:
            return el[self.attr]

        return el.string

    def clean_val(self, val):
        if val:
            return val.strip()

    def to_external(self, val):
        if self.r:
            found = re.search(self.r, val)
            if not found:
                raise exceptions.ParsingException()
            return found.group(1)

        return val

    def get_raw_value(self, body):
        try:
            return body.select(self.select)[0]
        except Exception:
            raise exceptions.ParsingException()

    def get(self, body):
        self.val = self.extracted_attr(self.get_raw_value(body))
        self.val = self.clean_val(self.val)
        return self.to_external(self.val)


class IntMapperXPathField(MapperXpathField):

    def to_external(self, val):
        ext_val = super().to_external(val)
        if ext_val:
            return int(ext_val)
