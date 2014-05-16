#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'PedroCarmona'


#imports

import time
from pcarmona.sum_sub_int_see import *
from pcarmona.init_pop import *
from pcarmona.utilities import *
from pcarmona.fitness import *
# Algoritmo genetico

def run_parents_selection(numb_runs, filename,pop_size, cromo_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener):
    with open(filename,'w') as f_data:
        f_data.write('one_point_cross, uniform_cross\n')
        for i in range(numb_runs):
            print('RUN...%s' % (i+1))
            initial_pop = init_pop(pop_size, cromo_size, cromo_int)
            best_1 = sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method[0], select_survivors, max_gener)
            best_2 = sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method[1], select_survivors, max_gener)
            f_data.write("%.15f" % best_1[1] + ', ' + "%.15f" % best_2[1] + '\n')
        f_data.close()
        show(filename)

# show results
def show(filename):
    with open(filename,'r') as f_data:
        data_1 = []
        data_2 = []
        for line in f_data:
            data = line[:-1].split(', ')
            data_1.append(str(data[0]))
            data_2.append(str(data[1]))
        plt.grid(True)
        plt.title('Rastrigin')
        plt.xlabel('Run')
        plt.ylabel('Best')
        plt.plot(data_1, label='One-point')
        plt.plot(data_2,label='Uniform')
        plt.legend(loc='upper left')
        plt.show()

# ---------------------------- EVOLUTIONARY ALGORITHM --------------------------------------------------
def sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func)
    for gener in range(max_gener):
        mates = select_parents(population,pop_size,3)
        offspring = crossover(mates, prob_cross, cross_method)
        offspring = mutation(offspring, prob_muta,muta_method)
        offspring = eval_pop(offspring,fitness_func)
        population = select_survivors(population, offspring)
    best_individual = best_pop(population)
    return best_individual


#quanto menor tamnho do array melhor
#soma igual a x?
#soma dos elementos todos da solucao e a aproximacao a x


def mutacao():
    pass


def recombinacao():
    pass



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

    # 1º TESTE FIXO
    # cruzamento = 0.9
    # mutacao = 0.1

    # 2º TESTE PROBABILIDADE INICIAL E FINAL
    # cruzamento = 0.8 durante 70% das gerações, 0 nas seguintes
    # mutacao = 0      durante 70% das gerações, 0.05 nas seguintes

    # 3º TESTE PROBABILIDADES VARIAVEIS
    # cruzamento  a descer de 0.9 a 0.7,  0.5, 0.3
    # mutacao     a descer de 0.01, 0.05, 0.1, 0.2
    # quatro pares de valores
    # definir como é feita a variação

    numb_runs          = 10

    file_name = 'out/'+  timestamp + '.csv'

    pop_size           = 10
    # pop_size           = 150
    cromo_size         = 10
    # cromo_size         = 10
    fitness_func       = knapsack_fitness
    prob_cross         = 0.8
    prob_muta          = 0.01
    select_parents     = tournament_sel
    muta_method        = muta_reals_rastrigin
    cross_method       = one_point_cross, uniform_cross
    select_survivors   = survivors_steady_state
    max_gener          = 100

    run_parents_selection(numb_runs, filename,pop_size, cromo_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener)

    pass
