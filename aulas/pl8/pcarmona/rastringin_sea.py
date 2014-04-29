#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
jb_sea.py
Um GA mesmo muito simples para problemas com representação binária.
Torneio. Elitism.

Pedro Carmona

com base em:
Ernesto Costa Março 2014!
"""

__author__ = 'pcarmona'
__date__ = 'March 2014'


import matplotlib
from pylab import *
from random import random,randint, shuffle, uniform,sample, gauss
from operator import itemgetter
import numpy
from math import sqrt
from copy import deepcopy


def sea(numb_generations,size_pop, populacao,size_cromo, gene_domain,prob_mut,prob_cross,selection,recombination,mutation,survivors, fit_func, phenotype,elite,t_size):
  if int(size_pop * elite) == 0:
      print('No Elitism will be used!!!')

  # evaluate population
  populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
  populacao.sort(key=itemgetter(1), reverse = False) # Maximizing!

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
          filhos = [[indiv[0], fit_func(indiv[0])] for indiv in filhos]
          progenitores.extend(filhos)
      # ------ Mutation
      descendentes = []

      for cromo,fit in progenitores:
          novo_cromo = deepcopy(cromo)
          #novo_cromo = mutation(cromo,prob_mut)
          prob_muta = 0.3
          novo_cromo = mutation(novo_cromo, prob_muta, gene_domain)
          descendentes.append((novo_cromo,0))
      descendentes = [ [indiv[0], fit_func(indiv[0])] for indiv in descendentes]
      descendentes.sort(key=itemgetter(1), reverse = False)
      # New population
      populacao = survivors(populacao,descendentes,elite)
      # Evaluate and sort
      populacao = [[indiv[0], fit_func(indiv[0])] for indiv in populacao]
      populacao.sort(key=itemgetter(1), reverse = False) # Maximizing

      #plot
      best_fit = populacao[0][1]
      avg_fit =  average(populacao)
      bests.append(best_fit)
      averages.append(avg_fit)

  #print("Individual: %s\nSize: %s\nFitness: %4.2f\nViolations:%d" % (phenotype(populacao[0][0]), len(phenotype(populacao[0][0])), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))
  #print("NGeracoes: %s\nIndivíduo: %s\nMérito: %4.2f\nViolações:%d\n------" % (numb_generations,phenotype(populacao[0][0]), populacao[0][1],viola(phenotype(populacao[0][0]), size_cromo)))

  return bests,averages


def cromo_reals(size, domain):
  indiv = [uniform(domain[0],domain[1]) for i in range(size)]
  return indiv

# Representation by binary strings
def gera_indiv(size_cromo,domain):
  #
  indiv = cromo_reals(size_cromo, domain)
  #binary
  #indiv = [randint(0,1) for i in range(size_cromo)]
  return indiv

# mutation: chromosome

def muta_reals(indiv, prob_muta, domain, sigma= 0.5):
    cromo = indiv[:]
    for i in range(len(cromo)):
       cromo[i] = muta_reals_gene(cromo[i],prob_muta, domain, sigma)
    return cromo

def muta_reals_gene(gene,prob_muta, domain_gene, sigma_gene):
    value = random()
    if value < prob_muta:
        muta_value = gauss(0,sigma_gene)
        new_gene = gene + muta_value
        if new_gene < domain_gene[0]:
            new_gene = domain_gene[0]
        elif new_gene > domain_gene[1]:
            new_gene = domain_gene[1]
        return new_gene
    else:
        return value



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

def uniform_cross(cromo_1, cromo_2,prob_cross):
  value = random()
  if value < prob_cross:
    f1=[]
    f2=[]
    for i in range(0,len(cromo_1)):
      if random() < 0.5:
        f1.append(cromo_1[i])
        f2.append(cromo_2[i])
      else:
        f1.append(cromo_2[i])
        f2.append(cromo_1[i])

    return [f1,f2]
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
  pool.sort(key=itemgetter(1), reverse=False)
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


def display_data(data1,data2, data3, data4):
  """Plot the data"""
  x1 = list(range(len(data1)))
  x2 = list(range(len(data2)))
  x3 = list(range(len(data3)))
  x4 = list(range(len(data4)))
  plt.grid(True)
  plt.plot(x1,data1, 'r')
  plt.plot(x2,data2, 'b')
  plt.plot(x3,data3, 'g')
  plt.plot(x4,data4, 'y')
  plt.show()

def avg_of_avg(avg_matrix):
  sum = numpy.sum(avg_matrix,axis=0)
  return sum/len(avg_matrix)

def fitness_rastrigin(indiv):
  #rastrigin = 0
  #A = 10
  #for gene in indiv:
  #  rastrigin = (gene**2 - A* np.cos(2*3.14159*gene))
  #rastrigin = A*len(indiv)
  #print(rastrigin)
  #return rastrigin
  A=10.0
  #print ind
  #indcromo = indiv[0]
  resultado = A * len(indiv) + sum([ xi**2-A*cos(2*pi*xi) for xi in indiv ])
  #print(-1*resultado)
  return -1*resultado;




if __name__ == '__main__':
  """This is just one example of values of the parameters..."""
  #size_pop= 10
  #size_cromo= 20
  #numb_generations = 30

  #size_pop= 2000
  #size_cromo= 30
  #numb_generations = 50

  #best_of_bests = []
  #avg_matrix = []
  #for i in range(0,30):
  #    bests,averages = sea(numb_generations, size_pop,size_cromo,0.3,0.7,tournament_selection,one_point_cross,muta_bin,survivors_elitism, fitness,phenotype, 0.02,3)
  #    best_of_bests = max(bests,best_of_bests)
  #    avg_matrix.append(averages)

  #avgs = avg_of_avg(avg_matrix)
  #display_data(bests,avgs)

  size_pop= 100
  size_cromo= 10
  numb_generations = 30
  gene_domain = [-5.12, 5.12]
  prob_mut = 0.3
  prob_cross = 0.7


  best_of_bests_one_point = []
  avg_matrix_one_point = []

  best_of_bests_one_point = []
  avg_matrix_one_point = []
  best_of_bests_uniform = []
  avg_matrix_uniform = []

  for i in range(0,10):
      populacao = [(gera_indiv(size_cromo,gene_domain),0) for j in range(size_pop)]

      bests_one_point,averages_one_point = sea(numb_generations, size_pop,populacao,size_cromo,gene_domain,prob_mut,prob_cross,tournament_selection,one_point_cross,muta_reals,survivors_elitism, fitness_rastrigin,phenotype, 0.02,3)
      best_of_bests_one_point = max(bests_one_point,best_of_bests_one_point)
      avg_matrix_one_point.append(averages_one_point)

      bests_uniform,averages_uniform = sea(numb_generations, size_pop,populacao,size_cromo,gene_domain,prob_mut,prob_cross,tournament_selection,uniform_cross,muta_reals,survivors_elitism, fitness_rastrigin,phenotype, 0.02,3)
      best_of_bests_uniform = max(bests_uniform,best_of_bests_uniform)
      avg_matrix_uniform.append(averages_uniform)

  avgs_one_point = avg_of_avg(avg_matrix_one_point)
  avgs_uniform = avg_of_avg(avg_matrix_uniform)
  display_data(bests_one_point,avgs_one_point, bests_uniform, avgs_uniform)
