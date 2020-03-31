import server.db_connecter as dbc
import pandas as pd

db = dbc.DBConnector()

def generate_dict():
  table_data = db.get_data()

  tokens = []
  for sentence in table_data['caption']:
    tokens += sentence.split(' ')
  dict_set = set(tokens)

  return {word: i for i, word in enumerate(dict_set) if word}

def select_words():
  d = generate_dict()
  with open('server/util/google_dict.txt', 'r') as file:
    lines = file.readlines()
  google_dict = [line[:-1] for line in lines]

  missing_words = 0
  for word in d:
    if word not in google_dict:
      add = True if input('Would you like to add "' + word + '"?').lower() == 'y' else False
      if add:
        with open('server/util/google_dict.txt', 'a') as file:
          file.write(word + '\n')
      else:
        missing_words += 1
  print('Words  missing from google dictionary:', missing_words)

if __name__ == '__main__':
  select_words()