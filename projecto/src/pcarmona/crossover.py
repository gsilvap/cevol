from copy import deepcopy
from numpy import *
import random

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
    """
        thinking in changing this function because when the position of the crossover
        is 0 or the last, there are not actual crossover verified, the cromossoms
        remain as before.
    """
    value = random.random()
    if value < prob_cross:
        pos = random.randint(0,len(cromo_1))
        #print ("...on crossover.."+str(pos))
        #antes = cromo_1, cromo_2
        f1 = cromo_1[0:pos] + cromo_2[pos:]
        f2 = cromo_2[0:pos] + cromo_1[pos:]
        depois1 = f1,f2
        depois2 = cromo_1, cromo_2
        #print (antes != depois1)
        #print (antes == depois2)
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

if __name__ == '__main__':
    import init_pop
    import fitness
    import parent_selection

    sizes              = array([5, 8, 4, 11, 6, 12])
    max_size           = 20
    pop_size           = 10
    cromo_size         = len(sizes)
    fitness_func       = fitness.subset_fitness
    select_parents     = parent_selection.tournament_sel

    initial_pop = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
    population = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)
    mates = select_parents(population,pop_size,3)
    prob_cross         = 0.8
    cross_method       = one_point_cross, uniform_cross

    offspring = crossover(mates, prob_cross, cross_method[0])
    offspring = crossover(mates, prob_cross, cross_method[1])

    [print (i) for i in offspring]
