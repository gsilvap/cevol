#! /usr/bin/env python


"""
my_pso_2014.py
Implementation of the standard PSO (CEC 2007). Global neighborhood.
Ernesto Costa, April 2014.
"""

# imports
from pylab import *
from random import uniform, random
from copy import deepcopy
from math import sqrt,sin,cos,pi
from operator import itemgetter

# colect and display
def run(numb_runs,numb_generations,numb_particles,weight_inertia, phi_1,phi_2,vel_max, domain, function,type_problem):
    # Colect Data
    print('Wait, please ')
    statistics_total = [pso(numb_generations,numb_particles,weight_inertia, phi_1,phi_2,vel_max, domain, function,type_problem) for i in range(numb_runs)]
    print("That's it!")
    # Process data: best and average by generation
    results = list(zip(*statistics_total))   
    best = [type_problem([result[0] for result in generation]) for generation in results]
    best_average = [sum([result[0] for result in generation])/numb_runs for generation in results]
    average = [sum([indiv[1] for indiv in genera])/numb_runs for genera in results]
    # Mostra
    ylabel('Fitness')
    xlabel('Generation')
    tit = 'Runs: %d , Phi: %0.2f, Vel: %0.2f' % (numb_runs,phi_1, vel_max)
    title(tit)
    axis= [0,numb_generations,0,len(domain)]
    p1 = plot(best,'r-o',label="Best")
    p2 = plot(average,'g->',label="Average")
    p3 = plot(best_average, 'y-s',label="Average of Best")
    if type_problem == max:
        legend(loc='lower right')
    else:
        legend(loc='upper right')
    show()
    
# main program

def pso(numb_generations,numb_particles,weight_inertia, phi_1,phi_2,vel_max, domain, function,type_problem):
    """
    num_generations = number of generations
    numb_particles = number of particles (10 + 2 * sqrt(dimensions)) or [10,50]
    weight_inertia (w) = to control oscilations (0.721 or [0,1[)
    phi_1, phi_2 = cognitive and social weights (1.193 or less than (12* w* (w-1) / (5*w -7)) or sum equal to 4)
    vel_max = maximum variation for move
    domain = [...,(inf_i,sup_i)...] domain values for each dimension
    function = to compute the fitness of a solution candidate
    type_problem = max or min, for maximization or minimization problems.
    
    Structures:
    particles = [...,[[...,p_i_j,...],fit_i],...], current position and fitness of particle i
    velocities = [..., [...,v_i_j,...],...]
    best_past = [...,[[...,p_i_j,...],fit_i],...], previous best position and fitness of particle i
    global_best = [[...,p_k_j,...],fit_k], position and fitness of the global best particle
    statistics_by_generation = [...,[best_fitness_gen_i, average_fitness_gen_i], ...]
    """
    # initialization
    numb_dimensions = len(domain)
    particles = [[generate_particle(domain),0] for count in range(numb_particles)]
    velocities = [generate_velocity(vel_max, numb_dimensions) for count in range(numb_particles)]
    
    # first evaluations
    particles = [[part, function(part)] for [part,fit] in particles]
    best_past = deepcopy(particles)
    
    # statistics
    statistics_by_generation = []
    
    # Run!
    for gen in range(numb_generations):
        # for each particle
        for part in range(numb_particles): 
            # compute the global best. 
            global_best = find_global_best(best_past, type_problem) 
            # for each dimension
            for dim in range(numb_dimensions):
                # update velocity
                velocities[part][dim] = weight_inertia * velocities[part][dim] 
                + phi_1 * (best_past[part][0][dim] - particles[part][0][dim])
                + phi_2 * (global_best[0][dim] - particles[part][0][dim])
                # update position
                particles[part][0][dim] = particles[part][0][dim] + velocities[part][dim]
                # clampling
                if particles[part][0][dim] < domain[dim][0]:
                    particles[part][0][dim] = domain[dim][0]
                    velocities[part][dim] = 0
                elif particles[part][0][dim] > domain[dim][1]:
                    particles[part][0][dim] = domain[dim][1]
                    velocities[part][dim] = 0
            # update fitness particle
            particles[part][1] = function(particles[part][0])
            # update best past
            if type_problem == max:
                # maximization situation
                if particles[part][1] > best_past[part][1]:
                    best_past[part] = deepcopy(particles[part])
                    # new global best?
                    if best_past[part][1] > global_best[1]:
                        global_best = best_past[part]
            else: # minimization problem
                if particles[part][1] < best_past[part][1]:
                    best_past[part] = deepcopy(particles[part])
                    # new global best?
                    if best_past[part][1] < global_best[1]:
                        global_best = best_past[part]
        # update statistics
        generation_average_fitness = sum([particle[1] for particle in best_past])/numb_particles
        generation_best_fitness = global_best[1]
        statistics_by_generation.append([generation_best_fitness,generation_average_fitness])
    # give me the best!
    print('\nBest Solution: %s\nFitness: %0.2f' % (global_best[0],global_best[1]))
    return statistics_by_generation
    

    
# Utilities

def generate_particle(domain):
    """ randomly construct a particle."""
    particle = [uniform(inf,sup) for inf,sup in domain]
    return particle

def generate_velocity(vel_max, numb_dimensions):
    """ randomly define the velocity of a particle."""
    velocity = [uniform(-vel_max,vel_max) for count in range(numb_dimensions)]
    return velocity

def find_global_best(best_past,type_problem):
    """ index of the best (according to fitness)."""
    aux = deepcopy(best_past)
    aux.sort(key=itemgetter(1))
    if type_problem == max:
        return aux[-1]
    else:
        return aux[0]


def clamping(indiv, domain):
    """keep individual's values inside the domain."""
    new_indiv = [verify(indiv[i],domain[i]) for i in range(len(indiv))]
    return new_indiv

def verify(value,domain_value):
    if value < domain_value[0]:
        return domain_value[0]
    elif value > domain_value[1]:
        return domain_value[1]
    else:
        return value
  
# ----------------------------- Test  Functions  -------------------------


# Sphere
def de_jong_f1_3d(indiv):
    """Sphere. domínio [[-5.12,5.12],[-5.12,5.12],[-5.12,5.12]]"""
    # validate values. Clip if outside bounds.
    x = indiv[0]
    y = indiv[1]
    z = indiv[2]
    if (x < -5.12) or (x > 5.12) or (y < -5.12) or (y > 5.12) or (z < -5.12) or (z > 5.12):
	    return 0
    else:
        f = indiv[0]**2 + indiv[1]**2 + indiv[2]**2
        return f

# Rosenbrock  
def de_jong_f2_2d(indiv):
    """ Rosenbrock. domínio [[-2.048,2.048],[-2.048,2.048]]"""
    # validate values. Clip if outside bounds.
    x = indiv[0]
    y = indiv[1]
    if (x < -2.048) or (x > 2.048) or (y < -2.048) or (y >2.048):
	    return 0
    else:
        f = 100* (indiv[0]**2 - indiv[1])**2 + (1 - indiv[0])**2
        return f
    
    
# -- Michaelewicz	
def michalewicz_1d(indiv):
    x=indiv[0]
    if (x < -1) or (x >2):
        return 0
    else:
        f= x * sin(10 * pi * x) + 1.0
        return f
	

def michalewicz_2d(indiv):
    """ Máximo = 38.85."""
    x=indiv[0]
    y=indiv[1]
    if (x < -3.0) or (x >12.1) or (y < 4.1) or (y > 5.8):
        return 0
    else:
        f= x * sin(4 * pi * x) + y* sin(20 *pi * y) + 21.5
        return f

# Rastringin   
def rastringin_3d(indiv):
    """ Rastringin. Domínio [(-5.12,5.12),(-5.12,5.12),(-5.12,5.12)]."""
    # validate values. Clip if outside bounds.
    x=indiv[0]
    y = indiv[1]
    z = indiv[2]
    if (x < -5.12) or (x > 5.12) or (y < -5.12) or (y > 5.12) or (z < -5.12) or (z > 5.12):
        return 0
    else:
        f = 3 * 10.0 + (x**2 - 10.0 * cos(2*pi*x)) + (y**2 - 10.0 * cos(2*pi*y)) + (z**2 - 10.0 * cos(2*pi*z))
        return f  
	
def rastringin_nd(indiv):
    """ Rastringin. Domínio [(-5.12,5.12),(-5.12,5.12),(-5.12,5.12)]."""
    n = len(indiv)
    # keep values inside the domain
    domain = [[-5.12,5.12] for i in range(n)]
    new_indiv = clamping(indiv,domain)
    f = n * 10.0 + sum([(x**2 - 10.0 * cos(2*pi*x)) for x in new_indiv])
    return f


# -------------------- Interface --------------------

# Cities,their coordinates, kept in a file of type tsp

def get_coordinates_tsp(filename):
    """ Obtain the cities' coordinates from a file in tsp format."""
    file_in = open(filename)
    data = file_in.readlines()
    coordinates = []
    for line in data[7:-1]:
        n,x,y = line[:-1].split()
        coordinates.append((float(x),float(y)))
    file_in.close()
    return coordinates

def dict_cities(coordinates):
    """ Create a dictionsary. Key = city identifier, value = coordinates."""
    my_dict = {}
    for i, (x,y) in enumerate(coordinates):
        my_dict[i] = (x,y)
    return my_dict

#  Fitness calculation
def phenotype(genotype,dict_cities):
    """ Obtaing the phenotype = list of coordinates."""
    pheno = [dict_cities[city] for city in genotype]
    return pheno


def distance(cid_i, cid_j):
    """ Euclidian distance."""
    x_i, y_i = cid_i
    x_j, y_j = cid_j
    dx = x_i - x_j
    dy = y_i - y_j
    dist = sqrt(dx**2 + dy**2)
    return dist

def evaluate(tour):
    numb_cities = len(tour)
    dist = 0
    for i in range(numb_cities):
        j = (i+1) % numb_cities
        dist  += distance(tour[i],tour[j])
    return dist

#um individuo é um conjunto de permutacoes
#geramos um individuo com random keys
def tsp_ncities(indiv):
    n = len(indiv)
    # keep values inside the domain
    domain = [[0,1] for i in range(n)]
    new_indiv = clamping(indiv,domain)
    permutation = decode_rk(indiv)
    print (permutation)
    f = phenotype(permutation,cities)
    return f

def decode_rk(vector):
    aux = deepcopy(vector)
    aux.sort()
    permutation = [vector.index(elem)+1 for elem in aux]
    return permutation

def generate_vector(size):
    return [random() for count in range(size)]


def main(filename):
    coordinates = get_coordinates_tsp(filename)
    global cities
    cities = dict_cities(coordinates)
    numb_iter = 50
    numb_ants = len(cities)
    #numb_ants = 50
    domain = [(0,1) for i in range(len(cities))]
    print (domain)
    print (cities[20])
    run(5,50,50,0.7,1.3,2.7,0.8,domain,tsp_ncities,min)



if __name__== '__main__':

    main('Berlin52.tsp')

    #run(10,100,30,1,2,2,0.8,[[-2.048,2.048],[-2.048,2.048]],de_jong_f2_2d,min)
    #run(5,50,50,0.7,1.3,2.7,0.8,[(-5.12,5.12),(-5.12,5.12),(-5.12,5.12)],rastringin_nd,min)


    #Nao ha relacao entre floats e inteiros. random entre 0-1 e transforma

