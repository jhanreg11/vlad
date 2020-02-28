import re


def clean_blacklist():
  raw_words = ""
  with open('server/util/blacklist.txt', 'r') as file:
    raw_words = file.read()

  word_list = re.split(r'[\n,]', raw_words)
  word_set = set([word.strip() for word in word_list])
  sorted_list = sorted(list(word_set))

  with open('server/util/blacklist.txt', 'w') as file:
    for w in sorted_list:
      file.write(w + '\n')


def get_blacklist(clean=False):
  if clean:
    clean_blacklist()

  with open('server/util/blacklist.txt', 'r') as file:
    lines = file.readlines()
  return [line[:-1] for line in lines if line != '\n']


if __name__ == '__main__':
  clean_blacklist()
  print(get_blacklist())