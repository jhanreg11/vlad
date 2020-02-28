from server.util.blacklist_util import get_blacklist
import re


class ProfanityFilter:
  blacklist = get_blacklist(True)
  base_words = ['fuck', 'shit', 'bitch', 'cunt', 'dick', 'penis', 'nigger', 'nigga', 'pussy', 'nazi', 'gay', 'jizz']
  semi_bad_words = ['ass']
  add_ons = ['face', 'head', 'wad', 'er', 'sucker', 'puss', 'lord', 'nut', 'hole', 'ass']

  def __init__(self):
    patterns = []

    # sort all lists in descending order by length
    self.blacklist.sort(key=len, reverse=True)
    self.base_words.sort(key=len, reverse=True)
    self.semi_bad_words.sort(key=len, reverse=True)
    self.add_ons.sort(key=len, reverse=True)

    # add unforgivable bad words (no surrounding whitespace necessary)
    for word in self.base_words:
      for add_on in self.add_ons:
        patterns.append(self.leetify(word + add_on))
      patterns.append(self.leetify(word))

    # add forgivable bad words (need surrounding whitespace)
    for word in self.semi_bad_words:
      for add_on in self.add_ons:
        patterns.append(r'(?<!\S)' + self.leetify(word + add_on) + r'(?!\S)')
      patterns.append(r'(?<!\S)' + self.leetify(word) + r'(?!\S)')

    # add blacklist (special bad words not included above, need surrounding whitespace)
    for word in self.blacklist:
      patterns.append(r'(?<!\S)' + word + r'(?!\S)')

    final_pattern = '(' + '|'.join(patterns) + ')'
    self.regex = re.compile(final_pattern, re.IGNORECASE)

  def leetify(self, string):
    """
    adds leetspeak and extra character options to string.
    :param string: string to leetify and add possibility for repeated chars
    :return: str, regex pattern
    """
    as_list = [c for c in string]
    for i in range(len(as_list)):
      if as_list[i] == 'a':
        as_list[i] = '[4@a]'
      elif as_list[i] == 'b':
        as_list[i] = '[8b6]'
      elif as_list[i] == 'c':
        as_list[i] = '[(c]'
      elif as_list[i] == 'e':
        as_list[i] = '[3e]'
      elif as_list[i] == 'i' or as_list[i] == 'l':
        as_list[i] = '[il1\|]'
      elif as_list[i] == 'o':
        as_list[i] = '[o0]'
      elif as_list[i] == 's':
        as_list[i] = '[sz2]'

    return '+'.join(as_list)

  def has_profanity(self, text):
    iterator = self.regex.finditer(text)

    try:
      next(iterator)
      return True
    except StopIteration:
      return False

  def remove_profanity(self, text):
    return re.sub(self.regex, '', text).strip()