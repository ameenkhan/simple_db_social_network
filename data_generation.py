from random import randrange

def rng():
  res = set()
  while len(res) < 30:
    tmp = randrange(27)
    if tmp not in res:
      res.add(tmp)
      print(tmp)

def list_rng():
  i = 0
  while i < 1475:
    print(randrange(26) + 1)
    i += 1

list_rng()