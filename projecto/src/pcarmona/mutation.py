
# mutation

import random
import copy

#---------------- Mutation
def mutation(population, prob_muta, method):
    new_population = copy.deepcopy(population)
    offspring = []
    for i in range(len(population)):
        off = method(new_population[i][0],prob_muta)
        offspring.append([off,0])
    return offspring



# genérica
def muta_bin(indiv,prob_muta, muta_func):
  cromo = copy.deepcopy(indiv)
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
  cromo = copy.deepcopy(indiv)
  value = random.random()
  if value < prob_muta:
    index = random.sample(range(len(cromo)),2)
    index.sort()
    i1,i2 = index
    cromo[i1],cromo[i2] = cromo[i2], cromo[i1]
  return cromo

def muta_perm_scramble(indiv,prob_muta):
  cromo = copy.deepcopy(indiv)
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
  cromo = copy.deepcopy(indiv)
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
  cromo = copy.deepcopy(indiv)
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
    c1 = cromo_bin(10)
    print(c1)
    print(muta_bin(c1,1.0, muta_bin_gene))
    c2 = cromo_int(10)
    print(c2)
    print(muta_perm_insertion(c2,1.0))


