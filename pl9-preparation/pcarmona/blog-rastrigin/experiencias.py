__author__ = 'GonçaloSilva'

import copy
import random
import time
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt

# ----------------------------- EXPERIMENT --------------------------------------------------------------------------
def run_parents_selection(numb_runs, filename,pop_size, cromo_size, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener):
    with open(filename,'w') as f_data:
        f_data.write('one_point_cross, uniform_cross\n')
        for i in range(numb_runs):
            print('RUN...%s' % (i+1))
            initial_pop = init_pop(pop_size, cromo_size)
            best_1 = sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method[0], select_survivors, max_gener)
            best_2 = sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method[1], select_survivors, max_gener)
            f_data.write("%.15f" % best_1[1] + ', ' + "%.15f" % best_2[1] + '\n')
        f_data.close()
        show(filename)

# show results
def show(filename):
    with open(filename,'r') as f_data:
        data_1 = []
        data_2 = []
        for line in f_data:
            data = line[:-1].split(', ')
            data_1.append(str(data[0]))
            data_2.append(str(data[1]))
        plt.grid(True)
        plt.title('Rastrigin')
        plt.xlabel('Run')
        plt.ylabel('Best')
        plt.plot(data_1, label='One-point')
        plt.plot(data_2,label='Uniform')
        plt.legend(loc='upper left')
        plt.show()

# ---------------------------- EVOLUTIONARY ALGORITHM --------------------------------------------------
def sea(initial_pop, fitness_func, prob_cross, prob_muta,select_parents, muta_method, cross_method, select_survivors, max_gener):
    pop_size = len(initial_pop)
    population = eval_pop(initial_pop, fitness_func)
    for gener in range(max_gener):
        mates = select_parents(population,pop_size,3)
        offspring = crossover(mates, prob_cross, cross_method)
        offspring = mutation(offspring, prob_muta,muta_method)
        offspring = eval_pop(offspring,fitness_func)
        population = select_survivors(population, offspring)
    best_individual = best_pop(population)
    return best_individual

# --------------------------- Auxiliary Functions
def init_pop(pop_size, cromo_size):
    """Return a list of individuals, where each indicidual has the forma [chromo, 0]"""
    population = [[cromo_reals(cromo_size),0] for count in range(pop_size)]
    return population

def cromo_reals(size):
    cromo =[random.uniform(-5.12,5.12) for i in range(size)]
    return cromo

def eval_pop(population,fitness_function):
    return [[indiv[0], fitness_function(indiv[0])] for indiv in population]

# -------------------------- Selection of Parents
def roulette_wheel(population, numb):
    """ Select numb individuals from the population
    according with their relative fitness. MIN """
    pop = copy.deepcopy(population)
    pop.sort(key=itemgetter(1))
    total_fitness = sum([indiv[1] for indiv in pop])
    mate_pool = []
    for i in range(numb):
        value = random.uniform(0,1)
        index = 0
        total = pop[index][1]/ total_fitness
        while total < value:
            index += 1
            total += pop[index][1]/total_fitness
        mate_pool.append(pop[index])
    return mate_pool

def tournament_sel(population, numb,t_size):
    mate_pool=[]
    for i in range(numb):
        indiv = tournament(population,t_size)
        mate_pool.append(indiv)
    return mate_pool

def tournament(population,t_size):
    """Deterministic. Minimization"""
    pool = random.sample(population, t_size)
    pool.sort(key=itemgetter(1))
    return pool[0]

# ---------------------------------- Genetic Operators
# ------------- Crossover
def crossover(population,prob_cross, method):
    new_population = copy.deepcopy(population)
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
def mutation(population,prob_muta, method):
    new_population = copy.deepcopy(population)
    offspring = []
    for i in range(len(population)):
        off = method(new_population[i][0],prob_muta)
        offspring.append([off,0])
    return offspring

def muta_reals_rastrigin(chromo, prob_muta):
    """For Rastrigin..."""
    new_chromo = copy.deepcopy(chromo)
    for i in range(len(new_chromo)):
        new_chromo[i] = muta_reals_gene(new_chromo[i],prob_muta, [-5.12,5.12], 1)
    return new_chromo

def muta_reals_gene(gene,prob_muta, domain_gene, sigma_gene):
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

# ------------------------------------- TEST FUNCTION
def rastrigin(x):
    """Rely on numpy arrays."""
    w = np.array(x)
    y= 10*len(w)+sum((w**2 - 10* np.cos(2*np.pi*w)))
    return y

if __name__ == "__main__":
    file_name = '/Users/pedrocarmona/semestre10/computacao-evolucionaria/cevol/pl9-preparation/pcarmona/blog-rastrigin/out'
    file_name =file_name + str(int(time.time()))
    file_name = file_name + '.csv'
    run_parents_selection(30,file_name, 150, 10, rastrigin, 0.8, 0.01,tournament_sel, muta_reals_rastrigin, [one_point_cross,uniform_cross], survivors_steady_state, 500)
