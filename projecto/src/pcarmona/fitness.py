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

def sub_fitness(pop):
  maxSize = 20

  #sizes = array([5, 8, 4, 11, 6, 12])
  sizes = array([1, 2, 3, 4, 5, 6])

  fitness = sum(sizes*pop,axis=0)
  fitness = where(fitness>maxSize,20-2*(fitness-maxSize),fitness)

  the_more_elements_in_less_its_fitness = - (sum(pop))

  fitness = fitness + the_more_elements_in_less_its_fitness

  return fitness

if __name__ == '__main__':
  a = array([1,1,0s,0,1,1])
  print(sub_fitness(a))

  #print(sub_fitness([0,0,0,0,0,0]))
  #print(sub_fitness([0,0,0,0,0,1]))
  #print(sub_fitness([0,0,0,0,1,0]))
  #print(sub_fitness([0,0,0,0,1,1]))
  #print(sub_fitness([0,0,0,1,0,0]))
  #print(sub_fitness([0,0,0,1,0,1]))
  #print(sub_fitness([0,0,0,1,1,0]))
  #print(sub_fitness([0,0,0,1,1,1]))
  #print(sub_fitness([0,0,1,0,0,0]))
  #print(sub_fitness([0,0,1,0,0,1]))
  #print(sub_fitness([0,0,1,0,1,0]))
  #print(sub_fitness([0,0,1,0,1,1]))
  #print(sub_fitness([0,0,1,1,0,0]))
  #print(sub_fitness([0,0,1,1,0,1]))
  #print(sub_fitness([0,0,1,1,1,0]))
  #print(sub_fitness([0,0,1,1,1,1]))
  #print(sub_fitness([0,1,0,0,0,0]))
  #print(sub_fitness([0,1,0,0,0,1]))
  #print(sub_fitness([0,1,0,0,1,0]))
  #print(sub_fitness([0,1,0,0,1,1]))
  #print(sub_fitness([0,1,0,1,0,0]))
  #print(sub_fitness([0,1,0,1,0,1]))
  #print(sub_fitness([0,1,0,1,1,0]))
  #print(sub_fitness([0,1,0,1,1,1]))
  #print(sub_fitness([0,1,1,0,0,0]))
  #print(sub_fitness([0,1,1,0,0,1]))
  #print(sub_fitness([0,1,1,0,1,0]))
  #print(sub_fitness([0,1,1,0,1,1]))
  #print(sub_fitness([0,1,1,1,0,0]))
  #print(sub_fitness([0,1,1,1,0,1]))
  #print(sub_fitness([0,1,1,1,1,0]))
  #print(sub_fitness([0,1,1,1,1,1]))
  #print(sub_fitness([1,0,0,0,0,0]))
  #print(sub_fitness([1,0,0,0,0,1]))
  #print(sub_fitness([1,0,0,0,1,0]))
  #print(sub_fitness([1,0,0,0,1,1]))
  #print(sub_fitness([1,0,0,1,0,0]))
  #print(sub_fitness([1,0,0,1,0,1]))
  #print(sub_fitness([1,0,0,1,1,0]))
  #print(sub_fitness([1,0,0,1,1,1]))
  #print(sub_fitness([1,0,1,0,0,0]))
  #print(sub_fitness([1,0,1,0,0,1]))
  #print(sub_fitness([1,0,1,0,1,0]))
  #print(sub_fitness([1,0,1,0,1,1]))
  #print(sub_fitness([1,0,1,1,0,0]))
  #print(sub_fitness([1,0,1,1,0,1]))
  #print(sub_fitness([1,0,1,1,1,0]))
  #print(sub_fitness([1,0,1,1,1,1]))
  #print(sub_fitness([1,1,0,0,0,0]))
  #print(sub_fitness([1,1,0,0,0,1]))
  #print(sub_fitness([1,1,0,0,1,0]))
  #print(sub_fitness([1,1,0,0,1,1]))
  #print(sub_fitness([1,1,0,1,0,0]))
  #print(sub_fitness([1,1,0,1,0,1]))
  #print(sub_fitness([1,1,0,1,1,0]))
  #print(sub_fitness([1,1,0,1,1,1]))
  #print(sub_fitness([1,1,1,0,0,0]))
  #print(sub_fitness([1,1,1,0,0,1]))
  #print(sub_fitness([1,1,1,0,1,0]))
  #print(sub_fitness([1,1,1,0,1,1]))
  #print(sub_fitness([1,1,1,1,0,0]))
  #print(sub_fitness([1,1,1,1,0,1]))
  #print(sub_fitness([1,1,1,1,1,0]))
