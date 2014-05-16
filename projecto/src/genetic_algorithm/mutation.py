
# mutation
from copy import deepcopy
from numpy import *
import random

#---------------- Mutation
def mutation(population, prob_muta, method):
    new_population = deepcopy(population)
    offspring = []
    for i in range(len(population)):
        off = method(new_population[i][0],prob_muta)
        offspring.append([off,0])
    return offspring



# genérica
def muta_bin(indiv,prob_muta, muta_func):
  cromo = deepcopy(indiv)
  for i in range(len(indiv)):
    cromo[i] = muta_func(cromo[i],prob_muta)
  return cromo

# binário
def muta_bin_gene(gene, prob_muta):
  g = gene
  value = random.random()
  if value < prob_muta:
    g ^= 1
  return g


# integers


# permutations

def muta_perm_swap(indiv, prob_muta):
  cromo = deepcopy(indiv)
  value = random.random()
  if value < prob_muta:
    index = random.sample(range(len(cromo)),2)
    index.sort()
    i1,i2 = index
    cromo[i1],cromo[i2] = cromo[i2], cromo[i1]
  return cromo

def muta_perm_scramble(indiv,prob_muta):
  cromo = deepcopy(indiv)
  value = random.random()
  if value < prob_muta:
    index = random.sample(range(len(cromo)),2)
    index.sort()
    i1,i2 = index
    scramble = cromo[i1:i2+1]
    random.shuffle(scramble)
    cromo = cromo[:i1] + scramble + cromo[i2+1:]
  return cromo


def muta_perm_inversion(indiv,prob_muta):
  cromo = deepcopy(indiv)
  value = random.random()
  if value < prob_muta:
    index = random.sample(range(len(cromo)),2)
    index.sort()
    i1,i2 = index
    inverte = []
    for elem in cromo[i1:i2+1]:
      inverte = [elem] + inverte
    cromo = cromo[:i1] + inverte + cromo[i2+1:]
  return cromo

def muta_perm_insertion(indiv, prob_muta):
  cromo = deepcopy(indiv)
  value = random.random()
  if value < prob_muta:
    index = random.sample(range(len(cromo)),2)
    index.sort()
    i1,i2 = index
    gene = cromo[i2]
    for i in range(i2,i1,-1):
      cromo[i] = cromo[i-1]
    cromo[i1+1] = gene
  return cromo




if __name__ == '__main__':
  import init_pop
  import fitness
  import parent_selection

  sizes              = array([5, 8, 4, 11, 6, 12])
  max_size           = 20
  pop_size           = 10
  cromo_size         = len(sizes)
  fitness_func       = fitness.subset_fitness
  select_parents     = parent_selection.tournament_sel

  initial_pop = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  c1 = population[0][0]
  print("############# muta_bin")
  print(c1)
  print(muta_bin(c1,1.0, muta_bin_gene))
  print("############# muta_perm_swap")
  print(c1)
  print(muta_perm_swap(c1,1.0))
  print("############# muta_perm_scramble")
  print(c1)
  print(muta_perm_scramble(c1,1.0))
  print("############# muta_perm_inversion")
  print(c1)
  print(muta_perm_inversion(c1,1.0))
  print("############# muta_perm_insertion")
  print(c1)
  print(muta_perm_insertion(c1,1.0))


