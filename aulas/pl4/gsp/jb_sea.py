#! /usr/bin/env python
 # -*- coding: utf-8 -*-

"""
jb_sea.py
Um GA mesmo muito simples para problemas com representaÃ§Ã£o binÃ¡ria.
Torneio. Elitism.
Ernesto Costa MarÃ§o 2014!
"""

__author__ = 'Ernesto Costa'
__date__ = 'March 2014'

import matplotlib.pyplot as plt
from pylab import *
from random import random,randint, shuffle, uniform,sample
from operator import itemgetter
from math import sqrt
import numpy as np


def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
    best = []
    avg = []
    generation = []

    # inicializa populaÃ§Ã£o: indiv = (cromo,fit)
    populacao = [(gera_indiv(size_cromo),0) for j in range(size_pop)]
    # avalia populaÃ§Ã£o
    populacao = [ [indiv[0], fit_func(indiv[0])] for indiv in populacao]
    populacao.sort(key=itemgetter(1), reverse = True) # MaximizaÃ§Ã£o

    for i in range(numb_generations):
      # selecciona progenitores
      mate_pool = selection(populacao, t_size)
       # Variation
       # ------ Crossover
      progenitores = []
      for j in  range(0,size_pop-1,2):
          cromo_1= mate_pool[j]
          cromo_2 = mate_pool[j+1]
          filhos = recombination(cromo_1,cromo_2, prob_cross)
          progenitores.extend(filhos)
      # ------ Mutation
      descendentes = []
      for indiv,fit in progenitores:

          novo_indiv = indiv[:]

          novo_indiv = mutation(indiv,prob_mut)
          descendentes.append((novo_indiv,0))
      descendentes = [ [indiv[0], fit_func(indiv[0])] for indiv in descendentes]
      descendentes.sort(key=itemgetter(1), reverse = True)
    	# Maximizacaoo
      # New population
      populacao = survivors(populacao,descendentes,elite)
      # Avalia e ordena nova _populaÃ§Ã£o
      populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
      populacao.sort(key=itemgetter(1), reverse = True) # MaximizaÃ§Ã£o

      bestAtual = populacao[0][1]
      avgAtual = sum(indiv[1] for indiv in populacao)/len(populacao)
      best.append(bestAtual)
      avg.append(avgAtual)
      generation.append(i)
    print("Individuo: %s\nMerito: %4.2f\nViolacoes: %d" % (phenotype(populacao[0][0]), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))

    #display_data(generation, best, avg)

    return phenotype(populacao[0][0]), populacao, best, avg


# RepresentaÃ§tuion by binary strings
def gera_indiv(size_cromo):
    indiv = [randint(0,1) for i in range(size_cromo)]
    return indiv

# mutation

def muta_bin(indiv,prob_muta):
    cromo = indiv[:]
    for i in range(len(indiv)):
        cromo[i] = muta_bin_gene(cromo[i],prob_muta)
    return cromo

# binÃ¡rio
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
		pos = randint(0,len(cromo_1))
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

# Fitness: JoÃ£o BrandÃ£o

def fitness(indiv):
    return evaluate(phenotype(indiv), len(indiv))

def phenotype(indiv):
    fen = [i+1 for i in range(len(indiv)) if indiv[i] == 1]
    return fen


def evaluate(indiv, comp):
    alfa = 1.5
    beta = -1
    #beta = -2
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

def display_data(generation, best, avg):
    """Plot the data"""
    #x = list(range(len(generation)))
    #plt.grid(True)
    plt.plot(generation,best,generation,avg)
    plt.show()


if __name__ == '__main__':
    #print(viola([1,3,4,9,10],10))
    #print(merito([1,0,1,1,0,0,0,0,1,1]))
    #print(viola([2, 5, 7, 14, 15, 17, 18, 19, 24, 25, 27, 30, 32, 33, 35, 36, 38, 39],40))
    #print(sea(500, 2000,10,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3))

    #data = [10, 25, 50, 100]
    generation = 10
    run = 5
    bestOfBest = []
    avgOfAvg = []
    avgOfAvgValues = []
    for i in range(0,run):
      bestSol, populacao, best, avg = sea(generation, 2000,50,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)

      avgOfAvg.append(avg)

      bestOfBest = max(bestOfBest, best)

    avgOfAvgValues = np.sum(avgOfAvg,axis = 0)/len(avgOfAvg[0])

    print(bestOfBest)
    print(avgOfAvgValues)


    display_data(range(0,generation), bestOfBest, avgOfAvgValues)




"""
aumentar elite
reduzir mutaçao

plot best of best and avg of avg

"""