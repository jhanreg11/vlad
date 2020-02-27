from server.util.blacklist_util import get_blacklist
import re

class ProfanityChecker:
  blacklist = get_blacklist(True)
  base_words = ['fuck', 'shit', 'bitch', 'cunt', 'dick', 'penis', 'nigger', 'nigga', 'pussy', 'nazi', 'ass', 'gay']
  add_ons = ['face', 'head', 'wad', 'er', 'sucker', 'puss', 'lord', 'nut']

  def __init__(self):
    self.blacklist_regex = re.compile('|'.join(self.blacklist), re.IGNORECASE)

    regexes = []
    for word in self.base_words:
      for add_on in self.add_ons + ['']:
        as_list = [c for c in word + add_on]

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

        regexes.append('+'.join(as_list))
    self.deriv_regex = re.compile('(' + '|'.join(regexes) + ')', re.IGNORECASE)

  def has_profanity(self, string):
    iterator = self.blacklist_regex.finditer(string)
    deriv_iter = self.deriv_regex.finditer(string)
    try:
      next(iterator)
      return True
    except StopIteration:
      try:
        next(deriv_iter)
        return True
      except StopIteration:
        return False