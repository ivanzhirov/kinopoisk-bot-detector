import crawler


def start():
    #  cap marvel 843859
    capitan_marvel = crawler.MovieVotePageCrawler(movie_id=843859)

    print(
        capitan_marvel.get_votes(max_count=110, prefetch_rules=[
            lambda user: user['vote'] and user['vote'] == 10,
        ], user_rules=[
            lambda user: user['movie_number'] <= 2
        ])
    )

    capitan_marvel.quit()


if __name__ == '__main__':
    start()
