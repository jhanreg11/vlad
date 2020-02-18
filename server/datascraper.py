import requests
import mysql.connector
import os

class RedditDataScraper:
    def __init__(self, subreddit, min_tokens, max_chars, db, valid_check, processs_fn):
        self.url = 'https://reddit.com/r/%s/'.format(subreddit)
        self.
