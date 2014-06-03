# -*- coding: utf-8 -*-

__author__ = 'Gonçalo Pereira, João Aguiar, Pedro Carmona'


#imports
from genetic_algorithm.init_pop import init_pop, cromo_bin
from genetic_algorithm.utilities import (
    init_project, create_sample_test, timestamp)
from genetic_algorithm.fitness import *
from genetic_algorithm.parent_selection import *
from genetic_algorithm.crossover import *
from genetic_algorithm.mutation import *
from genetic_algorithm.survivors import *
from genetic_algorithm.statistic import *

# Algoritmo genetico

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


def run_parents_selection(
        time_stamp_begin, numb_runs, pop_size, cromo_size, fitness_func,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size):

    filename_bests_of_run = (
        'out/' + time_stamp_begin + '_bests_of_run_generations('
        + str(max_gener) + ').csv')

    with open(filename_bests_of_run, 'w') as f_data:
        #f_data.write(
        #    'best_individual_case1, best_individual_case2, '
        #    + 'best_individual_case3\n')
        bests_matrix_1, averages_matrix_1 = init_runs_evaluation(max_gener,numb_runs)
        bests_matrix_2, averages_matrix_2 = init_runs_evaluation(max_gener,numb_runs)
        bests_matrix_3, averages_matrix_3 = init_runs_evaluation(max_gener,numb_runs)

        for current_run in range(numb_runs):
            print('RUN...%s' % (current_run+1))
            initial_pop = init_pop(pop_size, cromo_size, cromo_bin)
            best_1 = sea_first(
                initial_pop, fitness_func, select_parents, muta_method,
                cross_method, select_survivors, max_gener, sizes, max_size,
                bests_matrix_1, averages_matrix_1, current_run)

            best_2 = sea_second(
                initial_pop, fitness_func, select_parents, muta_method,
                cross_method, select_survivors, max_gener, sizes, max_size,
                bests_matrix_2, averages_matrix_2, current_run)

            best_3 = sea_third(
                initial_pop, fitness_func, select_parents, muta_method,
                cross_method, select_survivors, max_gener, sizes, max_size,
                bests_matrix_3, averages_matrix_3, current_run)
            f_data.write(
                "%.0f" % best_1[1] + ', ' + "%.0f" % best_2[1] + ', '
                + "%.0f" % best_3[1] + '\n')
        f_data.close()

    time_stamp_end = timestamp()
    save_statistics_and_create_graphs(
        ''+time_stamp_begin+'-'+time_stamp_end,
        bests_matrix_1, averages_matrix_1,
        bests_matrix_2, averages_matrix_2,
        bests_matrix_3, averages_matrix_3)


def sea_first(
        initial_pop, fitness_func, select_parents, muta_method, cross_method,
        select_survivors, max_gener, sizes, max_size, bests_matrix,
        averages_matrix, current_run):

    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)
    prob_cross = 0.8
    prob_muta = 0.01
    current_generation = 0
    population = generations(
        population, pop_size, fitness_func, prob_cross, prob_muta,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size, bests_matrix,
        averages_matrix, current_generation, current_run)
    best_individual = best_pop(population)
    return best_individual


def sea_second(
        initial_pop, fitness_func, select_parents, muta_method, cross_method,
        select_survivors, max_gener, sizes, max_size, bests_matrix,
        averages_matrix, current_run):

    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)

    prob_cross = 0.8
    prob_muta = 0
    max_gener_70 = int(max_gener*0.7)
    current_generation = 0
    population = generations(
        population, pop_size, fitness_func, prob_cross, prob_muta,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener_70, sizes, max_size, bests_matrix,
        averages_matrix, current_generation, current_run)

    prob_cross = 0
    prob_muta = 0.05
    max_gener_30 = max_gener - max_gener_70
    current_generation = max_gener_70
    population = generations(
        population, pop_size, fitness_func, prob_cross,
        prob_muta, select_parents, muta_method, cross_method,
        select_survivors, max_gener_30, sizes, max_size, bests_matrix,
        averages_matrix, current_generation, current_run)

    best_individual = best_pop(population)
    return best_individual


def generations(
        population, pop_size, fitness_func, prob_cross, prob_muta,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size, bests_matrix, averages_matrix, current_generation, current_run):
    for gener in range(max_gener):
        mates = select_parents(population, pop_size, 3)
        offspring = crossover(mates, prob_cross, cross_method)
        offspring = mutation(offspring, prob_muta, muta_method)
        offspring = eval_pop(offspring, fitness_func, sizes, max_size)
        population = select_survivors(population, offspring)
        evaluate_generation(
            population, bests_matrix, averages_matrix, current_generation +gener , current_run)
    return population

# ---------------------- EVOLUTIONARY ALGORITHM ---------------------------


def sea_third(
        initial_pop, fitness_func, select_parents, muta_method, cross_method,
        select_survivors, max_gener, sizes, max_size, bests_matrix,
        averages_matrix, current_run):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)
    cruz = [0.9, 0.7, 0.5, 0.3]
    mutacao = [0.01, 0.05, 0.1, 0.2]
    max_gener_interval = int(max_gener * 0.25)
    current_generation = 0
    for i in range(4):
        prob_cross = cruz[i]
        prob_muta = mutacao[i]
        current_generation = max_gener_interval * i
        #we cant forget!!! os restos da divisao
        if i == 3:
            max_gener_interval = max_gener - 3 * max_gener_interval
        population = generations(
            population, pop_size, fitness_func,
            prob_cross, prob_muta, select_parents,
            muta_method, cross_method,
            select_survivors, max_gener_interval,
            sizes, max_size, bests_matrix,
            averages_matrix, current_generation, current_run)

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
    """problem: sum subset of integers"""
    init_project()
    #sizes              = array([5, 8, 4, 11, 6, 12])
    MAX_SIZE = 50
    SIZES = create_sample_test(25, MAX_SIZE)
    print(SIZES)
    #array([5, 8, 4, 11, 6, 12])

    NUMBER_RUNS = 30
    TIMESTAMP = timestamp()
    POP_SIZE = 10
    # pop_size           = 150
    CROMO_SIZE = len(SIZES)
    # cromo_size         = 10
    FITNESS_FUNC = subset_fitness
    #prob_cross         = 0.8
    #prob_muta          = 0.01
    SELECT_PARENTS = tournament_sel
    MUTA_METHOD = muta_bin
    #cross_method       = one_point_cross, uniform_cross
    CROSS_METHOD = uniform_cross
    SELECT_SURVAVORS = survivors_steady_state
    MAX_GENER = 1000

    run_parents_selection(
        TIMESTAMP, NUMBER_RUNS, POP_SIZE, CROMO_SIZE, FITNESS_FUNC,
        SELECT_PARENTS, MUTA_METHOD, CROSS_METHOD, SELECT_SURVAVORS,
        MAX_GENER, SIZES, MAX_SIZE)
