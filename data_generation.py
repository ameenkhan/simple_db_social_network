from random import randrange

def rng():
  res = set()
  while len(res) < 30:
    tmp = randrange(27)
    if tmp not in res:
      res.add(tmp)
      print(tmp)

def list_rng():
  i = 1
  while i < 31:
    num_topics = randrange(6) + 1
    for x in range(num_topics):
      print(randrange(20) + 1)
    i += 1

list_rng()