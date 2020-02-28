from server.scrapers.datascraper import RedditDataScraper


class FiftyFiftyScraper(RedditDataScraper):
  def __init__(self):
    RedditDataScraper.__init__(self, 'FiftyFifty')

  def process(self, post):
    # TODO: get NSFW caption only, clear bad chars, super process
    pass