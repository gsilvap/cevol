import random

def cromo_bin(size):
  indiv = [random.randint(0,1) for i in range(size)]
  return indiv

def cromo_int(size):
  indiv = list(range(1,size + 1))
  random.shuffle(indiv)
  return indiv

def init_pop(pop_size, cromo_size, func):
  """Return a list of individuals, where each indicidual has the forma [chromo, 0]"""
  population = [[func(cromo_size),0] for count in range(pop_size)]
  return population

if __name__ == '__main__':
  print(init_pop(10,5,cromo_bin))
