from sqlalchemy.sql.sqltypes import _DateAffinity

__author__ = 'GonçaloSilva'

import time
from copy import deepcopy
from numpy import *
import random
from operator import itemgetter
import matplotlib.pyplot as plt

# ----------------------------- EXPERIMENT --------------------------------------------------------------------------
def run_parents_selection(numb_runs, filename,pop_size, cromo_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener):
    with open(filename,'w') as f_data:
        for i in range(numb_runs):
            print('RUN...%s' % (i+1))
            initial_pop = init_pop(pop_size, cromo_size)
            best_1 = sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method[0], select_survivors, max_gener)
            best_2 = sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method[1], select_survivors, max_gener)
            f_data.write(str(best_1[1])  + '\t' + str(best_2[1]) + '\n')
        f_data.close()
        show(filename)

# show results
def show(filename):
    with open(filename,'r') as f_data:
        data_1 = []
        data_2 = []
        for line in f_data:
            data = line[:-1].split()
            data_1.append(str(data[0]))
            data_2.append(str(data[1]))
        plt.grid(True)
        plt.title('Fitness')
        plt.xlabel('Run')
        plt.ylabel('Best')
        #plt.plot(data_1, label='One-point')
        #plt.plot(data_2,label='Uniform')
        #plt.legend(loc='upper left')
        plt.show()

# ---------------------------- EVOLUTIONARY ALGORITHM --------------------------------------------------
def sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func)
    # for i in range(len(population)):
    #             print(population[i])
    for gener in range(max_gener):
        mates = select_parents(population,pop_size,3)
        offspring = crossover(mates, prob_cross, cross_method)
        offspring = mutation(offspring, prob_muta,muta_method)
        offspring = eval_pop(offspring,fitness_func)
        # population = select_survivors(population, offspring)
    best_individual = best_pop(population)
    return best_individual

def init_pop(pop_size, cromo_size):
    population = [[cromo_bin(cromo_size),0] for count in range(pop_size)]
    return population

def cromo_bin(size):
    cromo =[random.randint(0,1) for i in range(size)]
    #print(cromo)
    return cromo

def eval_pop(population,fitness_function):
    return [[indiv[0], fitness_function(indiv[0])] for indiv in population]

# ---------------------------------- Genetic Operators
# ------------- Crossover
def crossover(population,prob_cross, method):
    new_population = deepcopy(population)
    offspring = []
    for i in range(0,len(population)-1,2):
        off_1,off_2 = method(new_population[i][0], new_population[i+1][0],prob_cross)
        offspring.extend([[off_1,0],[off_2,0]])
    if len(population)% 2 == 1:
        offspring.append(new_population[-1])
    return offspring

def one_point_cross(cromo_1, cromo_2,prob_cross):
    value = random.random()
    if value < prob_cross:
        pos = random.randint(0,len(cromo_1))
        f1 = cromo_1[0:pos] + cromo_2[pos:]
        f2 = cromo_2[0:pos] + cromo_1[pos:]
        return [f1,f2]
    else:
        return [cromo_1,cromo_2]

def uniform_cross(cromo_1, cromo_2,prob_cross):
    value = random.random()
    if value < prob_cross:
        f1=[]
        f2=[]
        for i in range(len(cromo_1)):
            if random.random() < 0.5:
                f1.append(cromo_1[i])
                f2.append(cromo_2[i])
            else:
                f1.append(cromo_2[i])
                f2.append(cromo_1[i])
        return [f1,f2]
    else:
        return [cromo_1,cromo_2]

#---------------- Mutation
def mutation(population, prob_muta, method):
    new_population = deepcopy(population)
    offspring = []
    for i in range(len(population)):
        off = method(new_population[i][0],prob_muta)
        offspring.append([off,0])
    return offspring

def muta_reals_rastrigin(chromo, prob_muta):
    """For Rastrigin..."""
    new_chromo = deepcopy(chromo)
    for i in range(len(new_chromo)):
        new_chromo[i] = muta_reals_gene(new_chromo[i],prob_muta, [-5.12,5.12], 1)
    return new_chromo

def muta_reals_gene(gene, prob_muta, domain_gene, sigma_gene):
    new_gene = gene
    value = random.random()
    if value < prob_muta:
        muta_value = random.gauss(0,sigma_gene)
        new_gene = gene + muta_value
        if new_gene < domain_gene[0]:
            new_gene = domain_gene[0]
        elif new_gene > domain_gene[1]:
            new_gene = domain_gene[1]
    return new_gene


# -------------------------- Selection of Parents
def tournament_sel(population, numb,t_size):
    mate_pool=[]
    for i in range(numb):
        indiv = tournament(population,t_size)
        mate_pool.append(indiv)
    return mate_pool

def tournament(population,t_size):
    """Deterministic. Minimization"""
    #print(population)
    #print(t_size)

    pool = random.sample(population, t_size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]

# ----------------------------------- Selection of Survivors
def survivors_generational(parents,offspring):
    return offspring

def survivors_steady_state(parents,offspring):
    """Minimizing."""
    size = len(parents)
    parents.extend(offspring)
    parents.sort(key=itemgetter(1))
    return parents[:size]

def best_pop(population):
    """minimization"""
    population.sort(key=itemgetter(1))
    return population[0]

def knapsack_fitness(pop):
    maxSize = 100
    #sizes = array([193.71,60.15,89.08,88.98,15.39,238.14,68.78,107.47,119.66,183.70])
    #sizes = array([109.60,125.48,52.16,195.55,58.67,61.87,92.95,93.14,155.05,110.89,13.34,132.49,194.03,121.29,179.33,139.02,198.78,192.57,81.66,128.90])
    sizes =[i for i in range(size)]

    #print("pop")
    #print(pop)

    fitness = sum([sizes[i] for i in range(len(sizes)) if pop[i] == 1])
    #fitness = where( fitness > maxSize, maxSize - 2 * (fitness - maxSize), fitness)

    # print(fitness)

    return fitness

"""
    Fazer 30 runs, medir o desempenho com:
    - qualidade do algoritmo
    - rapidez com que foi encontrado o melhor resultado

    Analise estatistica dos resultados e tirar conclusões
"""

# varicao das probabilidades de mutacao e recombinação
# mutação no inicio e recombinação no fim ?
if __name__ == '__main__':
    size = 10
    sequencia =[i for i in range(size)]

    # 1º TESTE FIXO
    # cruzamento = 0.9
    # mutacao = 0.1

    numb_runs          = 10
    filename          = 'cenas.csv'
    pop_size           = 10
    # pop_size           = 150
    cromo_size         = 10
    # cromo_size         = 10
    fitness_func       = knapsack_fitness
    prob_cross         = 0.9
    prob_muta          = 0.1
    select_parents     = tournament_sel
    muta_method        = muta_reals_rastrigin
    cross_method       = one_point_cross, uniform_cross
    select_survivors   = survivors_steady_state
    max_gener          = 100
    # max_gener          = 500

    run_parents_selection(numb_runs, filename,pop_size, cromo_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener)


    # 2º TESTE PROBABILIDADE INICIAL E FINAL
    # cruzamento = 0.8 durante 70% das gerações, 0 nas seguintes
    # mutacao = 0      durante 70% das gerações, 0.05 nas seguintes

    # 3º TESTE PROBABILIDADES VARIAVEIS
    # cruzamento  a descer de 0.9 a 0.7,  0.5, 0.3
    # mutacao     a descer de 0.01, 0.05, 0.1, 0.2
    # quatro pares de valores
    # definir como é feita a variação