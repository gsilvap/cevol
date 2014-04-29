"""
Numeros de Joao Brandao.

Algoritmo: Hill-climbing
Pertubation: best neighbor
Representation: binary

"""


__author__ = 'Ernesto Costa'
__date__ = 'February 2014'


import random

# Basic Hill Climbing

def jb_hc(problem_size, max_iter,fitness):
    candidate = random_indiv(problem_size)
    cost_candi = fitness(candidate,problem_size)
    for i in range(max_iter):
        next_neighbor = best_neighbor(candidate,fitness,problem_size)
        cost_next_neighbor = fitness(next_neighbor,problem_size)
        if cost_next_neighbor >= cost_candi:
            candidate = next_neighbor
            cost_candi = cost_next_neighbor
    return candidate


# Random Individual
def random_indiv(size):
    return [random.randint(0,1) for i in range(size)]

# Best neighbor
def best_neighbor(individual, fitness, problem_size):
    best = individual[:]
    best[0] = (best[0] + 1) % 2
    for pos in range(1,len(individual)):
        new_individual = individual[:]
        new_individual[pos]= (individual[pos] + 1) % 2
        if fitness(new_individual, problem_size) > fitness(best, problem_size):
            best = new_individual
    return best


# Fitness for JB
def evaluate(indiv,comp):
    alfa = 1
    beta = 1.5
    return alfa * sum(indiv) - beta * viola(fenotipo(indiv),comp)

def viola(indiv,comp):
    # count violations of constraints
    v = 0
    for elem in indiv:
        limite = min(elem-1,comp - elem)
        vi = 0
        for j in range(1,limite+1):
            if ((elem - j) in indiv) and ((elem+j) in indiv):
                vi += 1
        v += vi
    return v

# Auxiliar

def fenotipo(indiv):
    fen = [i+1 for i in range(len(indiv)) if indiv[i] == 1]
    return fen


if __name__ == '__main__':
    # For test purposes: beware of the time it may takes...
    res = fenotipo(jb_hc(100,10000,evaluate))
    quali = viola(res, len(res))
    print(quali,'\n', len(res), '\n',res)


