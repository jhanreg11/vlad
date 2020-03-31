import mysql.connector
import server.config as cfg
import pandas as pd


class DBConnector:
  """
  Class for connecting to sql server and storing data (link id, media url, caption) in server.
  create dict reddit_data={'username', 'password', 'database']} in config.py to use.
  """

  add_row_query = """INSERT INTO raw_data
  (link_id, media_url, caption) 
  VALUES (%(link_id)s, %(media_url)s, %(caption)s)"""

  create_table_query = """CREATE TABLE IF NOT EXISTS `raw_data` (
  `link_id` varchar(50) NOT NULL PRIMARY KEY,
  `media_url` varchar(255) NOT NULL,
  `caption` varchar(255) NOT NULL,
  """

  def __init__(self):
    try:
      self.connection = mysql.connector.connect(host='localhost',
                                           database=cfg.mysql_data['database'],
                                           user=cfg.mysql_data['username'],
                                           password=cfg.mysql_data['password'])
      if self.connection.is_connected():
        self.cursor = self.connection.cursor()
        print('connected to database!')
      else:
        raise Exception('Error creating cursor. Check connection and config.py')
    except Exception as e:
      print(e)

  def create_table(self):
    """
    create raw data table in db.
    :return: None
    """
    try:
      self.cursor.execute(self.create_table_query)
      self.cursor.commit()
    except mysql.connector.Error as e:
      print('Create table failed.\n ', e)

  def insert_data(self, data):
    """
    insert row or rows of data into clean_data table.
    :param data: list | dict, list of dicts or a single dict in form {'link_id', 'media_url', 'caption' }
    :return: None
    """
    # [print(post['caption']) for post in data if post['caption']]
    try:
      if isinstance(data, list):
        self.cursor.executemany(self.add_row_query, data)
      else:
        self.cursor.execute(self.add_row_query, data)
      self.connection.commit()

    except mysql.connector.Error as e:
      print(data)
      print(e)

  def get_data(self):
    """
    gets all data from raw_data table and returns in pandas dataframe.
    :return: pd.Dataframe
    """
    data = pd.DataFrame(columns=['fullname', 'media_url', 'caption'])
    query = 'SELECT * from raw_data'
    self.cursor.execute(query)

    for (link_id, media_url, caption) in self.cursor:
      data.loc[-1] = [link_id, media_url, caption]
      data.index += 1
    data = data.sort_index()

    return data

  def clear_data(self):
    """
    clear all rows from raw_data.
    :return: None
    """
    query = 'DELETE * FROM raw_data'
    self.cursor.execute(query)
    self.cursor.commit()
