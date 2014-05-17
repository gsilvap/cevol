import random
from operator import itemgetter


# -------------------------- Selection of Parents
def tournament_sel(population, numb,t_size):
    mate_pool=[]
    for i in range(numb):
        indiv = tournament(population,t_size)
        mate_pool.append(indiv)
    return mate_pool

def tournament(population,t_size):
    """Deterministic. Maximization"""
    #print(population)
    #print(t_size)

    pool = random.sample(population, t_size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]


if __name__ == '__main__':
    import init_pop
    import fitness
    from numpy import *
    import random

    sizes              = array([5, 8, 4, 11, 6, 12])
    max_size           = 20
    pop_size           = 10
    cromo_size         = len(sizes)
    fitness_func       = fitness.subset_fitness
    select_parents     = tournament_sel

    initial_pop = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
    population = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)
    print("len(population)="+str(len(population)))
    mates = select_parents(population,pop_size,3)
    print("len(mates)="+str(len(mates)))
    print (mates == population)

