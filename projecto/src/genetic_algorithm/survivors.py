# -*- coding: utf-8 -*-

from operator import itemgetter
from copy import deepcopy
from numpy import *
import random

# ----------------------------------- Selection of Survivors
def survivors_generational(parents,offspring):
    return offspring

def survivors_steady_state(parents,offspring):
    """Maximization."""
    size = len(parents)
    parents.extend(offspring)
    parents.sort(key=itemgetter(1), reverse=True)
    return parents[:size]

def best_pop(population):
    """Maximization"""
    population.sort(key=itemgetter(1), reverse=True)
    return population[0]

# Survivals: elitism
def survivors_elitism(parents,offspring,elite):
    """ Assumption: no size problems. Both populations are ordered by fitness."""
    size = len(parents)
    comp_elite = int(size* elite)
    new_population = parents[:comp_elite] + offspring[:size - comp_elite]
    return new_population




if __name__ == '__main__':
    import init_pop
    import fitness
    import parent_selection
    import crossover

    sizes              = array([5, 8, 4, 11, 6, 12])
    max_size           = 20
    pop_size           = 10
    cromo_size         = len(sizes)
    fitness_func       = fitness.subset_fitness
    select_parents     = parent_selection.tournament_sel

    initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
    population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)
    mates              = select_parents(population,pop_size,3)
    prob_cross         = 0.8
    cross_method       = crossover.one_point_cross, crossover.uniform_cross

    offspring = crossover.crossover(mates, prob_cross, cross_method[0])
    offspring = fitness.eval_pop(offspring,fitness_func, sizes, max_size)

    select_survivors   = survivors_steady_state

    population = select_survivors(population, offspring, 0.02)
    #[print (i) for i in offspring]
    print ("pop:")
    #[print (i) for i in population]
