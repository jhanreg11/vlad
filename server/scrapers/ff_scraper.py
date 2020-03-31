from server.scrapers.datascraper import RedditDataScraper
import re


class FiftyFiftyScraper(RedditDataScraper):
  def __init__(self):
    """
    Create a datascraper for https://reddit.com/r/FiftyFifty.
    """
    RedditDataScraper.__init__(self, 'FiftyFifty')
    self.nsfw_regex = re.compile(r'[\[(]?NSF[WL][\])]?', re.IGNORECASE)
    self.tags_regex = re.compile(r'[\[(]?N?SF[WL][\])]?|[\[(]50[/\\]50[)\]]', re.IGNORECASE)

  def process(self, post):
    new_caption = post['caption']
    midpoint = new_caption.index('|')
    nsfw_idx = self.nsfw_regex.search(new_caption).start()

    new_caption = new_caption[:midpoint] if nsfw_idx < midpoint else new_caption[midpoint:]

    new_caption = self.tags_regex.sub('', new_caption)

    post['caption'] = new_caption

    return RedditDataScraper.process(self, post)

  def validate(self, post):
    if RedditDataScraper.validate(self, post) and self.nsfw_regex.search(post['caption']):
      return True
    return False
