#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
jb_sea.py
Um GA mesmo muito simples para problemas com representação binária.
Torneio. Elitism.
Ernesto Costa Março 2014!
"""

__author__ = 'Ernesto Costa'
__date__ = 'March 2014'

import matplotlib
from pylab import *
from random import random,randint, shuffle, uniform,sample
from operator import itemgetter
import numpy
from math import sqrt
from copy import deepcopy


def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    if int(size_pop * elite) == 0:
        print('No Elitism will be used!!!')
    #  initialize population: [...,indiv,....] with indiv = (cromo,fit)
    populacao = [(gera_indiv(size_cromo),0) for j in range(size_pop)]
    # evaluate population
    populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
    populacao.sort(key=itemgetter(1), reverse = True) # Maximizing!

    #plot
    bests = []
    averages = []

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

        #plot
        best_fit = populacao[0][1]
        avg_fit =  average(populacao)
        bests.append(best_fit)
        averages.append(avg_fit)

    print("Individual: %s\nSize: %s\nFitness: %4.2f\nViolations:%d" % (phenotype(populacao[0][0]), len(phenotype(populacao[0][0])), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))
    print("NGeracoes: %s\nIndivíduo: %s\nMérito: %4.2f\nViolações:%d\n------" % (numb_generations,phenotype(populacao[0][0]), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))

    return bests,averages



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

def average(populacao):
    return sum([individuo[1] for individuo in populacao])/len(populacao)


def display_data(data1,data2):
    """Plot the data"""
    x1 = list(range(len(data1)))
    x2 = list(range(len(data2)))
    plt.grid(True)
    plt.plot(x1,data1, 'r')
    plt.plot(x2,data2, 'b')
    plt.show()

def avg_of_avg(avg_matrix):
    sum = numpy.sum(avg_matrix,axis=0)
    return sum/len(avg_matrix)

def construct_positions():
    return [[20833.3333, 17100.0000],[20900.0000, 17066.6667],[21300.0000, 13016.6667],[21600.0000, 14150.0000],[21600.0000, 14966.6667],[21600.0000, 16500.0000],[22183.3333, 13133.3333],[22583.3333, 14300.0000],[22683.3333, 12716.6667],[23616.6667, 15866.6667],[23700.0000, 15933.3333],[23883.3333, 14533.3333],[24166.6667, 13250.0000],[25149.1667, 12365.8333],[26133.3333, 14500.0000],[26150.0000, 10550.0000],[26283.3333, 12766.6667],[26433.3333, 13433.3333],[26550.0000, 13850.0000],[26733.3333, 11683.3333],[27026.1111, 13051.9444],[27096.1111, 13415.8333],[27153.6111, 13203.3333],[27166.6667, 9833.3333],[27233.3333, 10450.0000],[27233.3333, 11783.3333],[27266.6667, 10383.3333],[27433.3333, 12400.0000],[27462.5000, 12992.2222]]

def distance_matrix(locations):
    x = 0
    y = 1
    matriz = numpy.zeros(shape=(29,29))
    for i  in range(1,len(locations)):
        for j  in range(1,len(locations)):
            matriz[i][j] =


    for location1 in locations:
        for location2 in locations:
            dist_a_b = dist(a,b)


def dist(x1,y1, x2,):
    return numpy.sqrt(numpy.sum(x1,x2)**2,numpy.sum(y1,y2)**2)

def dist(x,y):
    return numpy.sqrt(numpy.sum((x-y)**2))

a = numpy.array((xa,ya,za))
b = numpy.array((xb,yb,zb))



if __name__ == '__main__':
    """This is just one example of values of the parameters..."""
    #size_pop= 10
    #size_cromo= 20
    #numb_generations = 30

    locations = construct_positions()


    #size_pop= 2000
    #size_cromo= 30
    #numb_generations = 50
    #
    #best_of_bests = []
    #avg_matrix = []
    #for i in range(0,30):
    #    bests,averages = sea(numb_generations, size_pop,size_cromo,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)
    #    best_of_bests = max(bests,best_of_bests)
    #    avg_matrix.append(averages)
    #
    #avgs = avg_of_avg(avg_matrix)
    #display_data(bests,avgs)
