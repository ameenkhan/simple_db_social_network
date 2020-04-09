from random import randrange

def rng():
  res = set()
  while len(res) < 30:
    tmp = randrange(27)
    if tmp not in res:
      res.add(tmp)
      print(tmp)

# print(randrange(5) + 2015)

def list_rng():
  i = 1
  while i < 1476:
    print(randrange(500) + 1)
    i += 1

list_rng()