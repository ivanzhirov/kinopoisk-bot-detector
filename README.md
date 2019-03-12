## Kinopoisk.ru crawler *with rules*

### Idea
The idea became after *Capitan Marvel* has been released. It seems like there were a lot of 10 votes on the movie with users with only one voted film in account and created right before the movie.

So i want to create a tool that can help to fetch that users(bots).

### Example
```python
import crawler

#  cap marvel 843859
capitan_marvel = crawler.MovieVotePageCrawler(movie_id=843859)

print(
    capitan_marvel.get_votes(max_count=900, prefetch_rules=[
        lambda user: user['vote'] and user['vote'] == 10,
    ], user_rules=[
        lambda user: user['movie_number'] <= 2
    ])
)

capitan_marvel.quit()
```

### Stack
- Python3.7
- Selenium + hub + chrome
- bs4
- skyZIP proxy

### Todo
tbd
### Knowing problems
tbd 
