"""ACO: simple version. Includes visualization."""

__author__ = 'Ernesto Costa'
__date__ = 'April 2014'


import matplotlib
from pylab import *
from random import random,randint, shuffle,choice
from operator import itemgetter
from math import sqrt

def run(num_runs, max_iter,problem,numb_ants,alpha=1.0, beta=2.5, rho=0.1):
    """"
    Send data to a file (best at the end) and show the output of the different runs (best and average by generation.
    """
    # Colect Data
    print('Wait, please ')
    statistics = [aco(max_iter,problem,numb_ants,alpha,beta,rho) for i in range(num_runs)]
    print("That's it!")
    # Data processing: best and average of bests by itertion
    results_iter = list(zip(*statistics))   
    bests = [min(iteration) for iteration in results_iter]
    average_bests = [sum(iteration)/float(num_runs) for iteration in results_iter]
    f_out = open('bests.txt','w')
    for i in range(max_iter):
        line = str(bests[i]) + '\n'
        f_out.write(line)
    f_out.close()
    # Show
    ylabel('Fitness')
    xlabel('Iteration')
    my_title = 'TSP by ACO %d Runs, Alpha: %0.2f, Beta: %0.2f, Rho: %0.2f' % (num_runs, alpha, beta, rho)
    title(my_title)
    axis= [0,max_iter,0,bests[0]]
    p1 = plot(bests,'r-o',label="Best")
    p2 = plot(average_bests,'g-s',label="Average")
    legend(loc='upper right')
    show()


def aco(max_iter,problem,numb_ants,alpha=1,beta=2.5,rho=0.1):
    """
    Typical values:
    alpha = 1
    beta = 2.5 (2..5)
    rho = 0.1 (0..1)
    numb_ants = |number cities|
    max_iter = maximum iterations
    problem = the dictionary with the coordinates of the cities    
    """
    # create heuristic solution
    number_cities = len(problem)
    best_tour = gera_tour(number_cities)
    best_cost = evaluate(phenotype(best_tour, problem))
    best_stat = [best_cost]
    # initialization - matrix of pheromone
    pheromone = initialize_pheromone(number_cities,best_cost)
    # Run!
    for i in range(max_iter):
        solutions = []
        for i in range(numb_ants):
	    # for each ant: build solution
            tour = incremental_build_tour(problem,pheromone,alpha, beta)
            tour_cost = evaluate(phenotype(tour,problem))
            solutions.append([tour, tour_cost])  
	    # update best
            if tour_cost < best_cost:
                best_tour = tour
                best_cost = tour_cost
	# update pheromone
        pheromone = evaporate(pheromone,rho)
        pheromone = update(pheromone,solutions)	
	# statistics
        best_stat.append(best_cost)
    print('Best Tour: %s\nBest Cost: %f'%(best_tour,best_cost))
    return best_stat
    
    

# Generate a tour as a permutation of integers
def gera_tour(tam_tour):
    tour = list(range(tam_tour))
    shuffle(tour)
    return tour

#  Initialize the pheromone matrix
def initialize_pheromone(number_cities, heuristic_value):
    tau_0 = number_cities / heuristic_value
    pheromone = [[tau_0] * number_cities for i in range(number_cities)]
    return pheromone

# Each ant build a tour from a random city
def incremental_build_tour(problem,pheromone,alpha,beta):
    numb_cities = len(problem)
    # where to start
    start_city = choice(list(range(numb_cities)))
    tour = [start_city]
    for i in range(numb_cities-1):
        candidates = calculate_possible_next_city(problem,tour[-1],tour,pheromone,alpha,beta)
        next_city = select_next_city(candidates)
        tour.append(next_city)
    return tour


def calculate_possible_next_city(problem,last_city,visited_cities, pheromone,alpha,beta):
    """Define an array of pairs [city, prob_(last,city)]."""
    numb_cities = len(problem)
    candidates = []
    for index,coord in problem.items():
        if index in visited_cities:
            continue
        prob_hist = pheromone[last_city][index] ** alpha
        dist_index = distance(problem[last_city],coord)
        prob_heur = (1.0 / dist_index)** beta
        probability= prob_hist * prob_heur
        candidates.append([index,probability])
    return candidates
	
def select_next_city(candidates):
    """Stochastic choice of the next city. Return its index."""
    total = sum([city[1] for city in candidates])
    if total == 0.0:
        return randint(0,len(candidates)-1)[1]
    probabilities = [[city[0],city[1]/total] for city in candidates]
    probabilities.sort(key=itemgetter(1))
    # Simulate a roulette wheel
    prob_reference = random()
    index = 0
    prob = probabilities[0][1]
    while prob < prob_reference:
        index += 1
        prob += probabilities[index][1]
    return probabilities[index][0]
    
    
# Update the pheromone matrix

def evaporate(pheromone,rho):
    return [ [(1.0 - rho) * tau_ik for tau_ik in city_i] for city_i in pheromone]

def update(pheromone,tours):
    Q= 8000
    for tour,cost in tours:
        delta_phero = Q/cost
        for index in range(len(tour)):
            i = tour[index]
            j = tour[(index + 1)% len(tour)]
            pheromone[i][j] += delta_phero
    return pheromone
	        
	    
    
    
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

def evaluate(tour):
    numb_cities = len(tour)
    dist = 0
    for i in range(numb_cities):
        j = (i+1) % numb_cities
        dist  += distance(tour[i],tour[j])
    return dist

def distance(cid_i, cid_j):
    """ Euclidian distance."""
    x_i, y_i = cid_i
    x_j, y_j = cid_j
    dx = x_i - x_j
    dy = y_i - y_j
    dist = sqrt(dx**2 + dy**2)
    return dist

# Tests

def main(numb_runs,filename):
    coordinates = get_coordinates_tsp(filename)
    cities = dict_cities(coordinates)
    numb_iter = 50
    numb_ants = len(cities)
    #numb_ants = 50
    run(numb_runs,numb_iter,cities,numb_ants,1,5,0.5)
    
if __name__ == '__main__':
    """
    coordinates = get_coordinates_tsp('Berlin52.tsp')
    # For Berlin52 the best tour is 7542 units
    cities = dict_cities(coordinates)
    numb_iter = 50
    #numb_ants = len(cities)
    numb_ants = 30
    print(aco(numb_iter,cities,numb_ants,1,2.5,0.1))
    """
    main(3,'Berlin52.tsp')

    
