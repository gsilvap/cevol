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

def subset_fitness(indiv, population, max_size):

  fitness = sum(population*indiv[0],axis=0)
  fitness = where(fitness>max_size,max_size-2*(fitness-max_size),fitness)

  the_more_elements_in_less_its_fitness = - (sum(indiv[0]))

  fitness = fitness + the_more_elements_in_less_its_fitness

  return fitness

def update_fitness(indiv, population, max_size, fitness_func):
  indiv[1] = fitness_func(indiv, population, max_size)


if __name__ == '__main__':
  #from professor example
  population = array([5, 8, 4, 11, 6, 12])
  max_size = 20
  # {8, 12}
  indiv1 = [array([0,1,0,0,0,1]),0]
  # {4, 5, 11}
  indiv2 = [array([1,0,1,1,0,0]),0]
  fitness_func = subset_fitness
  update_fitness(indiv1, population, max_size, fitness_func)
  update_fitness(indiv2, population, max_size, fitness_func)

  print(indiv1)
  print(indiv2)


