import mapper


class Contracts:
    def __init__(self, body):
        self.body = body

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
    total_votes: int = mapper.TotalMovieCountField(
        xpath='//*[@id="block_left"]/div/table/tbody/tr[3]/td/'
              'table[1]/tbody/tr[1]/td/table/tbody/tr/td/h2')


class UserContract(Contracts):
    movie_number: int = mapper.MapperXpathField(
        xpath='//*[@id="profileInfoWrap"]/div[3]/div/ul/li[1]/a/b')
    user_id: int = mapper.UserIDField(
        xpath='//*[@id="profileInfoWrap"]/div[1]/a')


class RatingItem(Contracts):
    user_id: int = mapper.UserIDField(xpath='td[2]/div/p/a')
    vote: int = mapper.MapperXpathField(xpath='td[3]/div/table/tbody/tr/td')
