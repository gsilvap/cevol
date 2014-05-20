#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Gonçalo Pereira, João Aguiar, Pedro Carmona'


#imports
from genetic_algorithm.init_pop import *
from genetic_algorithm.utilities import *
from genetic_algorithm.fitness import *
from genetic_algorithm.parent_selection import *
from genetic_algorithm.crossover import *
from genetic_algorithm.mutation import *
from genetic_algorithm.survivors import *

# Algoritmo genetico

def run_parents_selection(numb_runs, filename,pop_size, cromo_size, fitness_func, select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size):
    with open(filename,'w') as f_data:
        f_data.write('sea_first, sea_second, sea_third\n')
        for i in range(numb_runs):
            print('RUN...%s' % (i+1))
            initial_pop = init_pop(pop_size, cromo_size, cromo_bin)
            best_1 = sea_first(initial_pop, fitness_func, select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)
            best_2 = sea_second(initial_pop, fitness_func, select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)
            best_3 = sea_third(initial_pop, fitness_func, select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)
            print("%.15f" % best_1[1] + ', ' + "%.15f" % best_2[1]  + ', ' + "%.15f" % best_3[1] + '\n')
            print(str(best_1[0]) + ', ' + str(best_2[0])  + ', ' + str(best_3[0]) + '\n')
            f_data.write("%.15f" % best_1[1] + ', ' + "%.15f" % best_2[1]  + ', ' + "%.15f" % best_3[1] + '\n')
        f_data.close()
        show(filename)


def sea_first(initial_pop, fitness_func,select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size):

    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)
    prob_cross         = 0.8
    prob_muta          = 0.01
    generations(population, pop_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)
    best_individual = best_pop(population)
    return best_individual

def sea_second(initial_pop, fitness_func,select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)

    prob_cross         = 0.8
    prob_muta          = 0
    max_gener_70       = int(max_gener*0.7)

    generations(population, pop_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)

    prob_cross         = 0
    prob_muta          = 0.05
    max_gener_30       = int(max_gener*0.3)
    #we cant forget!!! os restos da divisao
    if max_gener_30+ max_gener_70 < max_gener:
        max_gener_30 += max_gener_70

    generations(population, pop_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)
    best_individual = best_pop(population)
    return best_individual

def generations(population, pop_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size):
    for gener in range(max_gener):
        mates = select_parents(population,pop_size,3)
        offspring = crossover(mates, prob_cross, cross_method)
        offspring = mutation(offspring, prob_muta,muta_method)
        offspring = eval_pop(offspring,fitness_func, sizes, max_size)
        population = select_survivors(population, offspring)

# ---------------------------- EVOLUTIONARY ALGORITHM --------------------------------------------------
def sea_third(initial_pop, fitness_func, select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)

    cruz = [0.9, 0.7,  0.5, 0.3]
    mutacao = [0.01, 0.05, 0.1, 0.2]

    gener_done = 0
    for i in range(4):
        prob_cross = cruz[i]
        prob_muta = mutacao[i]
        max_gener_interval = int(max_gener*0.25)
        gener_done += max_gener_interval
        #we cant forget!!! os restos da divisao
        if i == 3 and gener_done<max_gener:
            gener_done+= max_gener-gener_done
        generations(population, pop_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener_interval, sizes, max_size)
    best_individual = best_pop(population)
    return best_individual


"""
    Fazer 30 runs, medir o desempenho com:
    - qualidade do algoritmo
    - rapidez com que foi encontrado o melhor resultado

    Analise estatistica dos resultados e tirar conclusões
"""


# varicao das probabilidades de mutacao e recombinação
# mutação no inicio e recombinação no fim ?
if __name__ == '__main__':
    init_project()
    """
        problem: sum subset of integers
    """

    # 1º TESTE FIXO
    # cruzamento = 0.9
    # mutacao = 0.1



    # 2º TESTE PROBABILIDADE INICIAL E FINAL
    # cruzamento = 0.8 durante 70% das gerações, 0 nas seguintes
    # mutacao = 0      durante 70% das gerações, 0.05 nas seguintes




    # 3º TESTE PROBABILIDADES VARIAVEIS
    # cruzamento  a descer de 0.9 a 0.7,  0.5, 0.3
    # mutacao     a crescer de 0.01, 0.05, 0.1, 0.2
    # quatro pares de valores
    # definir como é feita a variação

    sizes              = array([5, 8, 4, 11, 6, 12])
    max_size           = 20

    numb_runs          = 10
    file_name = 'out/'+  timestamp() + '.csv'
    pop_size           = 10
    # pop_size           = 150
    cromo_size         = len(sizes)
    # cromo_size         = 10
    fitness_func       = subset_fitness
    #prob_cross         = 0.8
    #prob_muta          = 0.01
    select_parents     = tournament_sel
    muta_method        = muta_bin
    #cross_method       = one_point_cross, uniform_cross
    cross_method       = uniform_cross
    select_survivors   = survivors_steady_state
    max_gener          =500

    run_parents_selection(numb_runs, file_name,pop_size, cromo_size, fitness_func, select_parents, muta_method, cross_method, select_survivors, max_gener, sizes, max_size)

    pass
