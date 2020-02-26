from server.util.blacklist_util import get_blacklist
import re

class ProfanityChecker:
  blacklist = get_blacklist()

  def __init__(self):
    regex_words = []
    for word in self.blacklist:
      # allow for repeated characters of at least 1
      word_list = [c + '+' for c in word]

      # add poss l33tspeak char replacements
      for i in range(0, len(word_list), 2):
        if word_list[i] == 'e':
          word_list[i] = '[3e]'
        elif word_list[i] == 'a':
          word_list[i] = '[a@4]'
        elif word_list[i] == 'l':
          word_list[i] = '[1l]'

      regex_words.append(''.join(word_list))

    regex_pattern = '(' + '|'.join(regex_words) + ')'

    self.simple_regex = re.compile(regex_pattern, re.IGNORECASE)

  def has_profanity(self, string):
    iterator = self.simple_regex.finditer(string)
    try:
      next(iterator)
      return True
    except StopIteration:
      return False