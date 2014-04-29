#! /usr/bin/env python

"""
jb_sea.py
Um GA mesmo muito simples para problemas com representação binária.
Torneio. Elitism.
Ernesto Costa Março 2014!
"""

__author__ = 'Ernesto Costa'
__date__ = 'March 2014'

from pylab import *

from random import random, randint, shuffle, uniform, sample
#import random as rnd
import numpy as np

from operator import itemgetter
from math import sqrt
from copy import deepcopy

import matplotlib.pyplot as plt

def display(best,average):
    x = list(range(len(best)))
    plt.title('João Brandão using a Simple EA.')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.grid(True)
    plt.plot(x,best, label='Best')
    plt.plot(x,average, label='Average')
    plt.legend(loc='lower right')
    plt.show()

def run(numb_runs,numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    best,average = sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size)
    best_of_best = [best]
    average_of_average = [average]
    for i in range(numb_runs-1):
        best,average = sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size)
        best_of_best.append(best)
        average_of_average.append(average)
    print(best_of_best)
    best_by_gener = list(zip(*best_of_best))
    average_by_gener = list(zip(*average_of_average))
    data_best = [max(elem) for elem in best_by_gener]
    data_average = [sum(elem)/len(elem) for elem in average_by_gener]
    display(data_best, data_average)

def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    if int(size_pop * elite) == 0:
        print('No Elitism will be used!!!')
    #  initialize population: [...,indiv,....] with indiv = (cromo,fit)
    populacao = [(gera_indiv_tsp(size_cromo),0) for j in range(size_pop)]
    # evaluate population
    populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
    populacao.sort(key=itemgetter(1), reverse = True) # Maximizing!
    for j in range(numb_generations):
    # work with a copy of the population
        aux_populacao = deepcopy(populacao)
        # select parents
        mate_pool = selection(aux_populacao, t_size)
    # Variation
    # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            cromo_1= mate_pool[i][0]
            cromo_2 = mate_pool[i+1][0]
            filhos = recombination(cromo_1,cromo_2, prob_cross)
            progenitores.extend(filhos)
        # ------ Mutation
        descendentes = []
        for cromo,fit in progenitores:
            novo_cromo = cromo
            novo_cromo = mutation(cromo,prob_mut)
            descendentes.append((novo_cromo,0))
        descendentes = [ [indiv[0], fit_func(indiv[0])] for indiv in descendentes]
        descendentes.sort(key=itemgetter(1), reverse = True)
        # New population
        populacao = survivors(populacao,descendentes,elite)
        # Evaluate and sort
        populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
        populacao.sort(key=itemgetter(1), reverse = True) # Maximizing
    print("Individual: %s\nSize: %s\nFitness: %4.2f\nViolations:%d" % (phenotype(populacao[0][0]), len(phenotype(populacao[0][0])), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))
    return populacao[0][1], sum(indiv[1] for indiv in populacao)/len(populacao)
    #return best, average

"""
def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    best = []
    avg = []
    generation = []

    if int(size_pop * elite) == 0:
        print('No Elitism will be used!!!')
    #  initialize population: [...,indiv,....] with indiv = (cromo,fit)
    populacao = [(gera_indiv(size_cromo),0) for j in range(size_pop)]
    # evaluate population
    populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
    populacao.sort(key=itemgetter(1), reverse = True) # Maximizing!
    for j in range(numb_generations):
  # work with a copy of the population
        aux_populacao = deepcopy(populacao)
        # select parents
        mate_pool = selection(aux_populacao, t_size)
  # Variation
  # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            cromo_1= mate_pool[i][0]
            cromo_2 = mate_pool[i+1][0]
            filhos = recombination(cromo_1,cromo_2, prob_cross)
            progenitores.extend(filhos)
        # ------ Mutation
        descendentes = []
        for cromo,fit in progenitores:
            novo_cromo = cromo
            novo_cromo = mutation(cromo,prob_mut)
            descendentes.append((novo_cromo,0))
        descendentes = [ [indiv[0], fit_func(indiv[0])] for indiv in descendentes]
        descendentes.sort(key=itemgetter(1), reverse = True)
        # New population
        populacao = survivors(populacao,descendentes,elite)
        # Evaluate and sort
        populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
        populacao.sort(key=itemgetter(1), reverse = True) # Maximizing

        bestAtual = populacao[0][1]
        avgAtual = sum(indiv[1] for indiv in populacao)/len(populacao)
        best.append(bestAtual)
        avg.append(avgAtual)

    print("Individual: %s\nSize: %s\nFitness: %4.2f\nViolations:%d" % (phenotype(populacao[0][0]), len(phenotype(populacao[0][0])), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))

    return phenotype(populacao[0][0]), populacao, best, avg
    #return 0
"""


# Representation by binary strings
def gera_indiv(size_cromo):
    indiv = [randint(0,1) for i in range(size_cromo)]
    return indiv

# mutation: chromosome
def muta_bin(cromo,prob_muta):
    for i in range(len(cromo)):
        cromo[i] = muta_bin_gene(cromo[i],prob_muta)
    return cromo

#mutation: gene
def muta_bin_gene(gene, prob_muta):
    g = gene
    value = random()
    if value < prob_muta:
        g ^= 1
    return g

# Xover
def one_point_cross(cromo_1, cromo_2,prob_cross):
    # in: cromo, out: indiv
    value = random()
    if value < prob_cross:
      pos = randint(0,len(cromo_1))
      f1 = cromo_1[0:pos] + cromo_2[pos:]
      f2 = cromo_2[0:pos] + cromo_1[pos:]
      return [(f1,0),(f2,0)]
    else:
      return [(cromo_1,0),(cromo_2,0)]

# Tournament Selection
def tournament_selection(population,t_size):
    size= len(population)
    mate_pool = []
    for i in range(size):
        winner = tournament(population,t_size)
        mate_pool.append(winner)
    return mate_pool

def tournament(population,size):
    """Maximization Problem.Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]

# Survivals: elitism
def survivors_elitism(parents,offspring,elite):
    """ Assumption: no size problems. Both populations are ordered by fitness."""
    size = len(parents)
    comp_elite = int(size* elite)
    new_population = parents[:comp_elite] + offspring[:size - comp_elite]
    return new_population

# Fitness: João Brandão

def fitness(indiv):
    return evaluate(phenotype(indiv), len(indiv))

def phenotype(indiv):
    fen = [i+1 for i in range(len(indiv)) if indiv[i] == 1]
    return fen


def evaluate(indiv, comp):
    alfa = 1.5
    beta = -2
    return alfa * len(indiv) + beta * viola(indiv,comp)

def viola(indiv,comp):
    # Count violations using the phenotype
    v=0
    for elem in indiv:
      limite= min(elem-1,comp - elem)
      vi=0
      for j in range(1,limite+1):
        if ((elem - j) in indiv) and ((elem+j) in indiv):
          vi+=1
      v+=vi
    return v

"""
TSP Problem
"""

# Geracao individuos: TSP
def gera_indiv_tsp(size_cromo):
    indiv = [x for x in range(size_cromo)]
    shuffle(indiv)
    return indiv

# Fitness: TSP
def fitness_tsp(indiv):
    sum_dist = 0.0
    inicial = 0
    for i in range (len(indiv)):
        if i == 0:
            sum_dist += distancia[indiv.index(i)][indiv.index(len(indiv)-1)]
        else:
            sum_dist += distancia[indiv.index(i - 1)][indiv.index(i)]
    return sum_dist

# mutation: chromosome TSP
def muta_tsp(cromo,prob_muta):
    #for i in range(len(cromo)):
    #    cromo[i] = muta_tsp_gene(cromo[i], prob_muta)
    cromo = muta_tsp_gene(cromo, prob_muta)
    return cromo

#mutation: gene TSP
def muta_tsp_gene(gene, prob_muta):
    g = gene
    for i in range (len(gene) - 1):
        seed()
        value = random()
        if value < prob_muta:
            aux = g[i]
            g[i] = g[i+1]
            g[i+1] = aux
    return g
"""
# Xover
def one_point_cross(cromo_1, cromo_2,prob_cross):
    # in: cromo, out: indiv
    value = random()
    if value < prob_cross:
      pos = randint(0,len(cromo_1))
      f1 = cromo_1[0:pos] + cromo_2[pos:]
      f2 = cromo_2[0:pos] + cromo_1[pos:]
      return [(f1,0),(f2,0)]
    else:
      return [(cromo_1,0),(cromo_2,0)]
"""

# Roulette Wheel
def roulette_wheel(population):

    pass

def display_data(generation, best, avg):
    """Plot the data"""
    #x = list(range(len(generation)))
    #plt.grid(True)
    plt.plot(generation,best,generation,avg)
    plt.show()

if __name__ == '__main__':
    """ This is just one example of values of the parameters... """

    #berlin52.tsp
    #dados = [[1, 565.0, 575.0],[2, 25.0, 185.0],[3, 345.0, 750.0],[4, 945.0, 685.0],[5, 845.0, 655.0],[6, 880.0, 660.0],[7, 25.0, 230.0],[8, 525.0, 1000.0],[9, 580.0, 1175.0],[10, 650.0, 1130.0],[11, 1605.0, 620.0] ,[12, 1220.0, 580.0],[13, 1465.0, 200.0],[14, 1530.0, 5.0],[15, 845.0, 680.0],[16, 725.0, 370.0],[17, 145.0, 665.0],[18, 415.0, 635.0],[19, 510.0, 875.0]  ,[20, 560.0, 365.0],[21, 300.0, 465.0],[22, 520.0, 585.0],[23, 480.0, 415.0],[24, 835.0, 625.0],[25, 975.0, 580.0],[26, 1215.0, 245.0],[27, 1320.0, 315.0],[28, 1250.0, 400.0],[29, 660.0, 180.0],[30, 410.0, 250.0],[31, 420.0, 555.0],[32, 575.0, 665.0],[33, 1150.0, 1160.0],[34, 700.0, 580.0],[35, 685.0, 595.0],[36, 685.0, 610.0],[37, 770.0, 610.0],[38, 795.0, 645.0],[39, 720.0, 635.0],[40, 760.0, 650.0],[41, 475.0, 960.0],[42, 95.0, 260.0],[43, 875.0, 920.0],[44, 700.0, 500.0],[45, 555.0, 815.0],[46, 830.0, 485.0],[47, 1170.0, 65.0],[48, 830.0, 610.0],[49, 605.0, 625.0],[50, 595.0, 360.0],[51, 1340.0, 725.0],[52, 1740.0, 245.0]]

    #wi29.tsp
    dados = [[1 ,20833.3333 ,17100.0000],[2 ,20900.0000 ,17066.6667],[3 ,21300.0000 ,13016.6667],[4 ,21600.0000 ,14150.0000],[5 ,21600.0000 ,14966.6667],[6 ,21600.0000 ,16500.0000],[7 ,22183.3333 ,13133.3333],[8 ,22583.3333 ,14300.0000],[9 ,22683.3333 ,12716.6667],[10, 23616.6667, 15866.6667],[11, 23700.0000, 15933.3333],[12, 23883.3333, 14533.3333],[13, 24166.6667, 13250.0000],[14, 25149.1667, 12365.8333],[15, 26133.3333, 14500.0000],[16, 26150.0000, 10550.0000],[17, 26283.3333, 12766.6667],[18, 26433.3333, 13433.3333],[19, 26550.0000, 13850.0000],[20, 26733.3333, 11683.3333],[21, 27026.1111, 13051.9444],[22, 27096.1111, 13415.8333],[23, 27153.6111, 13203.3333],[24, 27166.6667, 9833.3333],[25, 27233.3333, 10450.0000],[26, 27233.3333, 11783.3333],[27, 27266.6667, 10383.3333],[28, 27433.3333, 12400.0000],[29, 27462.5000, 12992.2222]]
    distancia = [0.0]*len(dados)
    distancia = [distancia[:] for i in range (len(dados))]

    for i in range (len(dados)):
        for j in range (len(dados)):
            distancia[i][j] = sqrt((dados[i][1] - dados[j][1])**2 + (dados[i][2] - dados[j][2])**2)
            #print(distancia[i][j])
    #for i in range (len(dados)):
    #    print (distancia[i])

    #sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,
    #                    selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    sea(50,10,20,0.3,0.7,tournament_selection,one_point_cross,muta_tsp,survivors_elitism, fitness_tsp,phenotype, 0.02,3)
    #run(5,50,10,20,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness_tsp,phenotype, 0.02,3)

    #generation = 50
    #run(10,generation, 60,20,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)
    #sea(10, 10,20,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)
    #bestSol, populacao, best, avg = sea(10, 10,20,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)