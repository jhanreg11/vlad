def get_dict():
  with open('server/util/blacklist.txt', 'r') as file:
    lines = file.readlines()
  return [line[:-1] for line in lines if line != '\n']