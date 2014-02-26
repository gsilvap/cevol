""" PL3: single state stochastic algorithms."""

import random
from math import exp, sin, cos, pi


# --- HILL-CLIMBING
def basic_hc(problem_size, fitness, max_iter, neighbor_chooser, pesos, valores, capacidade):
    """Maximization."""
    candidate = random_candidate_bin_knapsack(problem_size, pesos, valores, capacidade)
    cost_candi = fitness(candidate, pesos, valores, capacidade)
    for i in range(max_iter):
        next_neighbor = neighbor_chooser(candidate, fitness)
        cost_next_neighbor = fitness(next_neighbor,pesos, valores, capacidade)
        if cost_next_neighbor >= cost_candi:
            candidate = next_neighbor
            cost_candi = cost_next_neighbor
    return candidate

def random_restart_hc(problem, fitness, max_iter,restart):
    candidate = random_candidate_bin(problem)
    cost_candidate = fitness(candidate)
    best = candidate
    cost_best = cost_candidate
    for i in range(1,max_iter+1,restart):
        j = 1
        while (j % restart) != 0:
            new_candidate = random_neighbor_bin(candidate)
            cost_new_candidate = fitness(new_candidate)
            if cost_new_candidate >= cost_candidate:
                candidate = new_candidate
                cost_candidate = cost_new_candidate
            j += 1
        if cost_candidate >= cost_best:
            best = candidate
            cost_best = cost_candidate
        candidate = random_candidate_bin(problem)
        cost_candidate = fitness(candidate)
    return best


# -- Neighborhood
# --- For local search
def random_neighbor_bin(individual, fitness):
    """Flip one position."""
    new_individual = individual[:]
    pos = random.randint(0,len(individual) - 1)
    gene = individual[pos]
    new_gene = (gene + 1) % 2
    new_individual[pos] = new_gene
    return new_individual

def best_neighbor_bin(individual, fitness):
    """Flip to the best neighbor."""
    for gene in range(0,len(individual)):
      new_individual = individual[:]
      gene = individual[pos]
      new_gene = (gene + 1) % 2
      new_individual[pos] = new_gene
      if pos==0 or fitness(new_individual) >= fitness(best_neighbor):
        best_neighbor = new_individual
    return best_neighbor

def random_neighbor_float(domain,individual,sigma=1):
    new_individual = individual[:]
    indice = random.randint(0, len(individual)-1)
    delta = random.gauss(0,sigma)
    while not (domain[indice][0] <= new_individual[indice] + delta <= domain[indice][1]):
        delta = random.gauss(0,sigma)
    new_individual[indice] += delta
    return new_individual

# -- Generate individuals

def random_candidate_bin(size):
    return [random.choice([0,1]) for i in range(size)]


def random_candidate_bin_knapsack(size, pesos, valores, capacidade):
    return [random.choice([0,1]) for i in range(size)]


def random_candidate_float(sp):
    return [random.uniform(sp[i][0],sp[i][1]) for i in range(len(sp))]

def random_candidate_permut(size):
    return random.shuffle(range(size))


# -- Evaluate individuals
def onemax(individual):
    """Individual = list of zeros and ones."""
    return sum(individual)

def de_jong_f1(individual):
    """
    De Jong F1 or the sphere function
    domain: [-5.12, 5.12] for each dimension.
    min = 0 at x = (0,0,...,0)
    """
    return sum([ x_i ** 2 for x_i in individual])

def knapsack_simple_fitness(individual, pesos, valores, capacidade):
    fitness = 0
    peso = 0
    for i in range(len(pesos)):
        if(individual[i]):
            fitness += valores[i]
            peso += pesos[i]
    return fitness if peso<capacidade else 0



if __name__ == '__main__':
    tam = [100,250,500]
    #array generator: [int(100*random.random()) for i in xrange(10)]
    pesos = [911, 863, 790, 637, 468, 897, 379, 626, 939, 273]
    valores = [55, 11, 51, 88, 30, 61, 95, 31, 60, 71]
    capacidade = sum(pesos)/2
    #print "capacidade: " + str(capacidade)
    problem_size = len(pesos)
    max_iter = 100
    print "###############"
    print "knapsack_simple_fitness and random neighbor:"
    solution = basic_hc(problem_size,knapsack_simple_fitness,max_iter, random_neighbor_bin, pesos, valores, capacidade)
    print solution
    print "fitness: " + str(knapsack_simple_fitness(solution,pesos, valores, capacidade))
    #print(basic_hc(problem_size,knapsack_simple_fitness,4, best_neighbor_bin, best))
    #print(random_restart_hc(20,onemax,200,30))

