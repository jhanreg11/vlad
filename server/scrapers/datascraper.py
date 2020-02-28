import requests
import server.config as cfg
import server.profanity_filter as pf
import server.db_connecter as dbc
class RedditDataScraper:
  """
  Collects, processes, and saves data from a reddit thread.
  add reddit_data={'username', 'password', 'app_name', 'app_secret', 'app_id'} to config.py in order to use.
  """

  max_chars = 255
  min_tokens = 5
  auth_url = 'https://www.reddit.com/'
  api_url = 'https://oauth.reddit.com/'

  def __init__(self, subreddit):
    """
    create a data scraper.
    :param subreddit: str, name of subreddit to read from.
    :param database: DBConnector, database object
    :param validate_fn: fn, function with single dict argument of a link to verify if it is valid to process and use.
    :param caption_process: fn, function with single string argument to perform any extra processing on caption before
    normal processing, returns new string.
    """
    self.subreddit = 'r/' + subreddit
    self.user_agent = f'{cfg.reddit_data["app_name"]} by {cfg.reddit_data["username"]}'
    self.access_token = ""
    self.set_access_token()
    self.db = dbc.DBConnector()
    self.profanity_filter = pf.ProfanityFilter()

  def run(self):
    """
    collects all listings from current subreddit, cleans them, then writes them to db.
    :return: bool, whether it was successful or not
    """
    listing = self.get_listing()
    while listing:
      self.db.insert_data([self.process(post) for post in listing if self.validate(post)])
      listing = self.get_listing(after=listing[-1]['link_id'])

  def validate(self, post):
    """
    validates a post is allowed to be
    :param post: dict, {
    :return:
    """
    if len(post['caption']) > self.min_tokens:
      return True
    else:
      return False

  def process(self, post):
    """
    processes a post to be placed in db.
    :param post: dict, {'link_id', 'media_url', 'caption'}
    :return: dict, processed post
    """
    post['caption'] = self.profanity_filter.remove_profanity(post['caption'])

    return post

  def set_access_token(self):
    """
    Obtain authorization for using reddit api.
    :return: None
    """
    data = {'grant_type': 'password',
            'username': cfg.reddit_data['username'],
            'password': cfg.reddit_data['password']}

    auth = requests.auth.HTTPBasicAuth(cfg.reddit_data['app_id'], cfg.reddit_data['app_secret'])

    r = requests.post(self.auth_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': self.user_agent},
                      auth=auth)

    response = r.json()
    self.access_token = 'bearer ' + response['access_token']

  def get_listing(self, before=None, after=None):
    """
    get listing of posts
    :param before: str, fullname of post to query before.
    :param after: str, fullname of post to query after
    :return: list,
    """
    headers = {'Authorization': self.access_token, 'User-Agent': self.user_agent}

    params = {'limit': 1000}
    if before:
      params['before'] = before
    elif after:
      params['after'] = after

    print('fetching listing...')
    response = requests.get(self.api_url + self.subreddit, headers=headers, params=params)

    if response.status_code == 200 and response.json()['data']['children']:
      print('successful, listing length:', len(response.json()['data']['children']))
      items = []
      links = response.json()['data']['children'] if before or after else response.json()['data']['children'][1:]

      for link in links:
        url_type = link['data']['url'][-4:]
        media_url = ''

        if url_type == '.jpg' or url_type == '.png' or url_type == 'webp':
          media_url = link['data']['url']
        elif 'secure_media' in link.keys() and 'fallback_url' in link['secure_media']['reddit_video'].keys():
          media_url = link['data']['secure_media']['reddit_video']['fallback_url']

        items.append({'link_id': 't3_' + link['data']['id'], 'media_url': media_url, 'caption': link['data']['title']})

      return items

    else:
      print('GET FAILED', response.json())
      return []

  def api_health_check(self):
    """
    Checks that API is connected and authorized properly.
    :return: bool, if API is connected/authorized
    """
    headers = {'Authorization': self.access_token, 'User-Agent': self.user_agent}
    response = requests.get(self.api_url + 'api/v1/me', headers=headers)
    if response.status_code == 200:
      return True
    else:
      return False
