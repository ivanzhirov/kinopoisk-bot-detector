import crawler


def start():
    #  cap marvel 843859
    capitan_marvel = crawler.MovieVotePageCrawler(movie_id=843859)
    capitan_marvel.fetch()

    print(
        capitan_marvel.get_votes(max_count=5, prefetch_rules=[
            lambda user: user.vote == 10,
        ], user_rules=[
            lambda user: user.movie_number == 1
        ])
    )

    capitan_marvel.quit()


if __name__ == '__main__':
    start()
