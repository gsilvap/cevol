# -*- coding: utf-8 -*-
from operator import itemgetter
import numpy


def init_generation_evaluation():
  generations_bests = []
  generations_averages = []
  return generations_bests,generations_averages


def evaluate_generation(population, generations_bests, generations_averages):
  # Evaluate and sort
  population.sort(key=itemgetter(1), reverse = False) # Maximizing
  #plot
  best_fit = population[0][1]
  avg_fit =  generation_average_fit(population)
  generations_bests.append(best_fit)
  generations_averages.append(avg_fit)

def generation_average_fit(population):
  return sum([indiv[1] for indiv in population])/len(population)

def init_runs_evaluation():
  #matrix with bests of each run per each
  runs_bests = []
  runs_averages = []
  return runs_bests,runs_averages

def average_of_run_per_generation(runs_averages):
  sum = numpy.sum(runs_averages,axis=0)
  return sum/len(runs_averages)

def best_of_run_per_generation(runs_averages):
  maxs = numpy.max(runs_averages,axis=0)
  return maxs

def evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages ):
  #print ("generations_bests")
  #print (runs_averages)
  #print ("runs_bests")
  #print (runs_bests)
  runs_bests.append(generations_bests)
  runs_averages.append(generations_averages)

def final_evaluation(runs_bests, runs_averages):
  averages_per_generation = average_of_run_per_generation(runs_averages)
  bests_per_generation = best_of_run_per_generation(runs_bests)

  return bests_per_generation, averages_per_generation
  #plot


def test_function_represents_one_run():
  generations_bests, generations_averages = init_generation_evaluation()

  import init_pop
  import fitness
  sizes              = numpy.array([5, 8, 4, 11, 6, 12])
  max_size           = 20
  pop_size           = 10
  cromo_size         = len(sizes)
  fitness_func       = fitness.subset_fitness
  initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  #generation 1...5
  evaluate_generation(population, generations_bests, generations_averages)

  initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  evaluate_generation(population, generations_bests, generations_averages)


  initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  evaluate_generation(population, generations_bests, generations_averages)

  initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  evaluate_generation(population, generations_bests, generations_averages)

  initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
  population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  evaluate_generation(population, generations_bests, generations_averages)

  return generations_bests,generations_averages


if __name__ == '__main__':
  runs_bests,runs_averages = init_runs_evaluation()

  generations_bests,generations_averages = test_function_represents_one_run()
  evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages)

  generations_bests,generations_averages = test_function_represents_one_run()
  evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages)

  generations_bests,generations_averages = test_function_represents_one_run()
  evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages)

  generations_bests,generations_averages = test_function_represents_one_run()
  evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages)

  generations_bests,generations_averages = test_function_represents_one_run()
  evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages)

  print ("runs_bests")
  print (runs_bests)
  print ("runs_averages")
  print (runs_averages)

  bests_per_generation, averages_per_generation = final_evaluation(runs_bests, runs_averages)

  print ("bests_per_generation")
  print (bests_per_generation)
  print ("averages_per_generation")
  print (averages_per_generation)

