from server.scrapers.datascraper import RedditDataScraper
import re
import random


class FearMeScraper(RedditDataScraper):
  """
  Create a datascraper for https://reddit.com/r/FearMe.
  """

  def __init__(self):
    RedditDataScraper.__init__(self, 'FearMe')
    self.pronoun_regex = re.compile(r'(?<!\S)(supplicants|s?he)(?!\S)', re.IGNORECASE)

  def process(self, post):
    post['caption'] = self.pronoun_regex.sub('the man' if random.random() > .5 else 'the woman', post['caption'])
    return RedditDataScraper.process(self, post)