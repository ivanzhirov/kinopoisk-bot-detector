import mapper


class Contracts:
    def __init__(self, body):
        self.body = body

    def to_dict(self):
        return {
            k: getattr(self, k).get(body=self.body)
            for k in dir(self)
            if issubclass(
                getattr(self, k).__class__,
                mapper.MapperXpathField
            )
        }


class MovieContract(Contracts):
    total_votes: int = mapper.TotalMovieCountField(
        xpath='//*[@id="block_left"]/div/table/tbody/tr[3]/td/'
              'table[1]/tbody/tr[1]/td/table/tbody/tr/td/h2')


class UserContract(Contracts):
    movie_number: int = mapper.MapperXpathField(
        xpath='//*[@id="profileInfoWrap"]/div[3]/div[1]/ul/li[1]/a/b')


class RatingItem(Contracts):
    user_id: int = mapper.UserIDField(xpath='td[2]/div/p/a')
    vote: int = mapper.MapperXpathField(xpath='td[3]/div/table/tbody/tr/td')
