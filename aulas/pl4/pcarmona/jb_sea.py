#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
jb_sea.py
Um GA mesmo muito simples para problemas com representação binaria.
Torneio. Elitism.
Ernesto Costa Marco 2014!
"""

__author__ = 'Ernesto Costa'
__date__ = 'March 2014'

import matplotlib
from pylab import *
import numpy as np
from random import random,randint, shuffle, uniform,sample
from operator import itemgetter
from math import sqrt

def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    # inicializa população: indiv = (cromo,fit)
    populacao = [(gera_indiv(size_cromo),0) for j in range(size_pop)]
    # avalia população
    populacao = [ [indiv[0], fit_func(indiv[0])] for indiv in populacao]
    populacao.sort(key=itemgetter(1), reverse = True) # Maximização

    bests = []
    averages = []

    for i in range(numb_generations):
        # selecciona progenitores
        mate_pool = selection(populacao, t_size)
       # Variation
       # ------ Crossover
        progenitores = []
        for j in  range(0,size_pop-1,2):
            cromo_1= mate_pool[j][:]
            cromo_2 = mate_pool[j+1][:]
            filhos = recombination(cromo_1,cromo_2, prob_cross)
            progenitores.extend(filhos)
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            novo_indiv = indiv[:]
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,0))

        descendentes = [ [indiv[0], fit_func(indiv[0])] for indiv in descendentes]
        descendentes.sort(key=itemgetter(1), reverse = True) # Maximização

        # New population
        populacao = survivors(populacao,descendentes,elite)
        # Avalia e ordena nova _população
        populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
        populacao.sort(key=itemgetter(1), reverse = True) # Maximização

        #print populacao
        best_fit = populacao[0][1]
        avg_fit =  average(populacao)
        bests.append(best_fit)
        averages.append(avg_fit)

    #display_data(bests,averages)

    print("NGeracoes: %s\nIndivíduo: %s\nMérito: %4.2f\nViolações:%d\n------" % (numb_generations,phenotype(populacao[0][0]), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))

    #return phenotype(populacao[0][0])
    return bests,averages


# Representaçtuion by binary strings
def gera_indiv(size_cromo):
    indiv = [randint(0,1) for i in range(size_cromo)]
    return indiv

# mutation

def muta_bin(indiv,prob_muta):
    cromo = indiv[:]
    for i in range(len(indiv)):
        cromo[i] = muta_bin_gene(cromo[i],prob_muta)
    return cromo

# binário
def muta_bin_gene(gene, prob_muta):
    g = gene
    value = random()
    if value < prob_muta:
        g ^= 1
    return g
# Xover

def one_point_cross(cromo_1, cromo_2,prob_cross):
	value = random()
	if value < prob_cross:
		pos = randint(0,len(cromo_1[0]))
		f1 = cromo_1[0][0:pos] + cromo_2[0][pos:]
		f2 = cromo_2[0][0:pos] + cromo_1[0][pos:]
		return [[f1,0],[f2,0]]
	else:
		return [cromo_1,cromo_2]

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
    """ Assunption: no size problems"""
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
    beta = -1
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
    sum = np.sum(avg_matrix,axis=0)
    return sum/len(avg_matrix)

if __name__ == '__main__':
    #print(viola([1,3,4,9,10],10))
    #print(merito([1,0,1,1,0,0,0,0,1,1]))
    #print(viola([2, 5, 7, 14, 15, 17, 18, 19, 24, 25, 27, 30, 32, 33, 35, 36, 38, 39],40))

    #print(sea(500, 2000,10,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3))
    size_pop= 10
    size_cromo= 20
    numb_generations = 10
    best_of_bests = []
    avg_matrix = []
    for i in range(0,10):
        bests,averages = sea(numb_generations, size_pop,size_cromo,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)
        best_of_bests = max(bests,best_of_bests)
        avg_matrix.append(averages)

    avgs = avg_of_avg(avg_matrix)
    display_data(bests,avgs)


