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
        time_stamp, numb_runs, pop_size, cromo_size, fitness_func,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size):

    filename_bests_of_run = (
        'out/' + time_stamp + '_bests_of_run_generations('
        + str(max_gener) + ').csv')

    with open(filename_bests_of_run, 'w') as f_data:
        f_data.write(
            'best_individual_case1, best_individual_case2, '
            + 'best_individual_case3\n')
        runs_bests_1, runs_averages_1 = init_runs_evaluation()
        runs_bests_2, runs_averages_2 = init_runs_evaluation()
        runs_bests_3, runs_averages_3 = init_runs_evaluation()

        for i in range(numb_runs):
            print('RUN...%s' % (i+1))
            initial_pop = init_pop(pop_size, cromo_size, cromo_bin)
            generations_bests_1, generations_averages_1 = (
                init_generation_evaluation())
            best_1 = sea_first(
                initial_pop, fitness_func, select_parents, muta_method,
                cross_method, select_survivors, max_gener, sizes, max_size,
                generations_bests_1, generations_averages_1)
            evaluate_run(
                runs_bests_1, runs_averages_1, generations_bests_1,
                generations_averages_1)

            generations_bests_2, generations_averages_2 = (
                init_generation_evaluation())
            best_2 = sea_second(
                initial_pop, fitness_func, select_parents, muta_method,
                cross_method, select_survivors, max_gener, sizes, max_size,
                generations_bests_2, generations_averages_2)
            evaluate_run(
                runs_bests_2, runs_averages_2, generations_bests_2,
                generations_averages_2)

            generations_bests_3, generations_averages_3 = (
                init_generation_evaluation())
            best_3 = sea_third(
                initial_pop, fitness_func, select_parents, muta_method,
                cross_method, select_survivors, max_gener, sizes, max_size,
                generations_bests_3, generations_averages_3)
            evaluate_run(
                runs_bests_3, runs_averages_3, generations_bests_3,
                generations_averages_3)
            f_data.write(
                "%.15f" % best_1[1] + ', ' + "%.15f" % best_2[1] + ', '
                + "%.15f" % best_3[1] + '\n')
        f_data.close()

    save_statistics_and_create_graphs(
        time_stamp, runs_bests_1, runs_averages_1, runs_bests_2,
        runs_averages_2, runs_bests_3, runs_averages_3)


def sea_first(
        initial_pop, fitness_func, select_parents, muta_method, cross_method,
        select_survivors, max_gener, sizes, max_size, generations_bests,
        generations_averages):

    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)
    prob_cross = 0.8
    prob_muta = 0.01
    population = generations(
        population, pop_size, fitness_func, prob_cross, prob_muta,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size, generations_bests,
        generations_averages)
    best_individual = best_pop(population)
    return best_individual


def sea_second(
        initial_pop, fitness_func, select_parents, muta_method, cross_method,
        select_survivors, max_gener, sizes, max_size, generations_bests,
        generations_averages):

    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)

    prob_cross = 0.8
    prob_muta = 0
    max_gener_70 = int(max_gener*0.7)

    population = generations(
        population, pop_size, fitness_func, prob_cross, prob_muta,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener_70, sizes, max_size, generations_bests,
        generations_averages)

    prob_cross = 0
    prob_muta = 0.05
    max_gener_30 = max_gener - max_gener_70

    population = generations(
        population, pop_size, fitness_func, prob_cross,
        prob_muta, select_parents, muta_method, cross_method,
        select_survivors, max_gener_30, sizes, max_size, generations_bests,
        generations_averages)

    best_individual = best_pop(population)
    return best_individual


def generations(
        population, pop_size, fitness_func, prob_cross, prob_muta,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size, generations_bests, generations_averages):
    for gener in range(max_gener):
        mates = select_parents(population, pop_size, 3)
        offspring = crossover(mates, prob_cross, cross_method)
        offspring = mutation(offspring, prob_muta, muta_method)
        offspring = eval_pop(offspring, fitness_func, sizes, max_size)
        population = select_survivors(population, offspring)
        evaluate_generation(
            population, generations_bests, generations_averages)
    return population

# ---------------------- EVOLUTIONARY ALGORITHM ---------------------------


def sea_third(
        initial_pop, fitness_func, select_parents, muta_method, cross_method,
        select_survivors, max_gener, sizes, max_size, generations_bests,
        generations_averages):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func, sizes, max_size)
    cruz = [0.9, 0.7, 0.5, 0.3]
    mutacao = [0.01, 0.05, 0.1, 0.2]
    max_gener_interval = int(max_gener * 0.25)
    for i in range(4):
        prob_cross = cruz[i]
        prob_muta = mutacao[i]
        #we cant forget!!! os restos da divisao
        if i == 3:
            max_gener_interval = max_gener - 3 * max_gener_interval
        population = generations(
            population, pop_size, fitness_func,
            prob_cross, prob_muta, select_parents,
            muta_method, cross_method,
            select_survivors, max_gener_interval,
            sizes, max_size, generations_bests,
            generations_averages)

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

    #sizes              = array([5, 8, 4, 11, 6, 12])
    max_size = 40
    sizes = create_sample_test(20, max_size)
    print(sizes)
    #array([5, 8, 4, 11, 6, 12])

    numb_runs = 30
    time_stamp = timestamp()
    time_stamp = "000"
    pop_size = 10
    # pop_size           = 150
    cromo_size = len(sizes)
    # cromo_size         = 10
    fitness_func = subset_fitness
    #prob_cross         = 0.8
    #prob_muta          = 0.01
    select_parents = tournament_sel
    muta_method = muta_bin
    #cross_method       = one_point_cross, uniform_cross
    cross_method = uniform_cross
    select_survivors = survivors_steady_state
    max_gener = 100

    run_parents_selection(
        time_stamp, numb_runs, pop_size, cromo_size, fitness_func,
        select_parents, muta_method, cross_method, select_survivors,
        max_gener, sizes, max_size)

    pass
