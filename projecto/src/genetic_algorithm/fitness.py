from numpy import *

def knapsack_fitness(pop):
  maxSize = 500
  #sizes = array([193.71,60.15,89.08,88.98,15.39,238.14,68.78,107.47,119.66,183.70])

  sizes = array([109.60,125.48,52.16,195.55,58.67,61.87,92.95,93.14,155.05,110.89,13.34,132.49,194.03,121.29,179.33,139.02,198.78,192.57,81.66,128.90])

  fitness = sum(sizes*pop,axis=0)
  fitness = where(fitness>maxSize,500-2*(fitness-maxSize),fitness)

  return fitness

def knapsack_simple_fitness(individual, pesos, valores, capacidade):
    fitness = 0
    peso = 0
    for i in range(len(pesos)):
        if(individual[i]):
            fitness += valores[i]
            peso += pesos[i]
    return fitness if peso<capacidade else 0

def subset_fitness(indiv, sizes, max_size):
  """these method receives an indiv and calculates is fitness.
  Indiv must be an array, with indiv[0] being its fenotype, and indiv[1] its current fitness
  firstly:
  - is calculated the size the indiv has,
  if its size is bigger than the max_size allowed,
  the for each 1 of size diference is decremented 2 to his fitness
  then
  - the more elements the indiv has, the less score he has,
  because he want individuals with minimization of cardinality
  """
  fitness = sum(sizes*indiv,axis=0)
  fitness = where(fitness>max_size,max_size-2*(fitness-max_size),fitness)

  the_more_elements_in_less_its_fitness = - (sum(indiv))

  fitness = fitness + the_more_elements_in_less_its_fitness

  return fitness


def eval_pop(population,fitness_function, sizes, max_size):
    return [[indiv[0], fitness_function(indiv[0],sizes, max_size)] for indiv in population]

if __name__ == '__main__':
  #from professor example
  #sizes = array([5, 8, 4, 11, 6, 12])
  #max_size = 20
  ## {8, 12}
  #indiv1 = [array([0,1,0,0,0,1]),0]
  ## {4, 5, 11}
  #indiv2 = [array([1,0,1,1,0,0]),0]
  #fitness_func = subset_fitness
  #print(indiv1)
  #print(indiv2)
  import init_pop

  sizes              = array([5, 8, 4, 11, 6, 12])
  max_size           = 20
  pop_size           = 10
  cromo_size         = len(sizes)
  fitness_func       = subset_fitness

  initial_pop = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population = eval_pop(initial_pop, fitness_func, sizes, max_size)

  print (population)



