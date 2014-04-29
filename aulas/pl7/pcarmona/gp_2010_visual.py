#! /usr/bin/env python
# -*-coding: utf-8 -*-

"""
gp_2010.py
Implementation of GP. Simple version. Inspired by tinyGP by R. Poli
Ernesto Costa, March 2010

Individuals are represented by a pair [indiv,fit]
where indiv is an individual represented recursively as a list of lists. For example, f(t_1,...,t_n)
is represented as [f, rep(t_1), ..., rep(t_n)]

"""
from pylab import *
from random import random, choice,uniform,sample
from types import FunctionType, ListType, FloatType, IntType,LongType, StringType
from operator import itemgetter
from copy import deepcopy



# Evolver
def gp(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,elite_size,seed=0):
    """
    Problem dependent data, i.e., terminal set, function set and fitness casesare kept in a file.
    Could be implemented as a class object...

    problem = file name where the data for the problem are stored
    num_gen = number of generations
    pop_size = population size
    in_max_depth = max depth for initial individuals
    max_len = maximum number of nodes
    prob_mut_node = mutation probability for node mutation
    prob_cross = crossover probability (mutation probability = 1 - prob_cross)
    t_size = tournament size
    elite_size = size of the elite
    seed = define seed for the random generator? Default = False.
    """
    # Not nice ...
    global min_rnd, max_rnd, function_set,vars_set
    # Extract information about the problem.  problem is the name of
    # the file where that information is stored
    # Fitness Cases = [[X1,...,Xn Y], ...]
    fit_cases = get_fit_cases(problem)
    # Header = Numb_Vars, Min_Rnd, Max_Rnd, Function_Set
    numb_vars, min_rnd,max_rnd,function_set = get_header(problem)
    vars_set = generate_vars(numb_vars)
    const_set = ['uniform(min_rnd,max_rnd)']
    terminal_set = vars_set + const_set
    # Define initial population
    individuals = ramped_half_and_half(function_set,terminal_set,pop_size, in_max_depth)

    # Evaluate population
    population = [[indiv,evaluate(indiv,fit_cases)] for indiv in individuals]
    statistics = []
    # Evolve
    for i in range(numb_gen):
	population.sort(key=itemgetter(1), reverse=True)
	# Statistics
	average_fitness = sum([indiv[1] for indiv in population])/ float(pop_size)
        best_fitness = population[0][1]
        statistics.append((best_fitness,average_fitness))
	print 'Best at Generation %d:\n%s\n----------------' % (i,population[0])

        # Select mating pool
        mate_pool = tournament_selection(population,t_size)
        # offspring after variation
	offspring = []
	for i in range(pop_size):
	    rnd = random()
	    if rnd < prob_cross:
		# subtree crossover
		parent_1 = tournament(population,t_size)[0]
		parent_2 = tournament(population,t_size)[0]
		new_offspring = subtree_crossover(parent_1, parent_2)
	    else: # prob mutation = 1 - prob crossover!
		# mutation
		parent = tournament(population,t_size)[0]
		new_offspring = point_mutation(parent,prob_mut_node)
	    offspring.append(new_offspring)
        # Evaluate new population (offspring)
        offspring = [[indiv,evaluate(indiv,fit_cases)] for indiv in offspring]
        # Merge parents and offspring
	population = survivors_elitism(population,offspring,elite_size)
    # Define Best
    population.sort(key=itemgetter(1), reverse=True)
    # Statistics
    average_fitness = sum([indiv[1] for indiv in population])/ float(pop_size)
    best_fitness = population[0][1]
    statistics.append((best_fitness,average_fitness))
    print 'FINAL BEST\n%s\n----------------' % population[0]
    return statistics



# Function Set Wrappers

class Func_wrapper(object):
    def __init__(self, function,arity,name):
	self.function = function
	self.arity = arity
	self.name = name

    def get_function(self):
	return self.function

    def get_arity(self):
	return arity

    def get_name(self):
	return self.name

    def __repr__(self):
	print 'Function: %s\nArity: %d\nName: %s' % (self.function, self.arity,self.name)

    def show_function(self):
	return self.__repr__()



def add_w(x,y):
	return x + y

def mult_w(x,y):
	return x * y

def sub_w(x,y):
    return x -y

def div_prot_w(x,y):
    if abs(y) <= 1e-3:
	return x
    else:
	return float(x)/y

# Variation operators

# Crossover

def sub_tree(tree,position):
    def sub_tree_aux(tree,position):
        global count
        if position == count:
            count = 0
            return tree
        else:
            count += 1
            if isinstance(tree,ListType):
                for i,sub in enumerate(tree[1:]):
                    res_aux = sub_tree(sub, position)
                    if res_aux:
                        break
                return res_aux
    return sub_tree_aux(tree,position)

def replace_sub_tree(tree, sub_tree_1, sub_tree_2):
    if tree == sub_tree_1:
        return sub_tree_2
    elif isinstance(tree, ListType):
        for i,sub in enumerate(tree[1:]):
            res = replace_sub_tree(sub, sub_tree_1, sub_tree_2)
            if res and (res != sub):
                return [tree[0]] + tree[1:i+1] + [res] + tree[i+2:]
        return tree
    else:
        return tree


def subtree_crossover(par_1,par_2):
    """ATENTION:if identical sub_trees replace the first ocorrence..."""
    global count
    # Choose crossover point (indepently)
    size_1 = indiv_size(par_1)
    size_2 = indiv_size(par_2)
    cross_point_1 = choice(range(size_1))
    cross_point_2 = choice(range(size_2))
    #print 'Cross 1: %d\tCross 2: %d' % (cross_point_1,cross_point_2)
    # identify subtrees to echange
    sub_tree_1 = sub_tree(par_1, cross_point_1)
    sub_tree_2 = sub_tree(par_2, cross_point_2)
    #print 'Subtree 1: %s\tSubtree 2: %s' % (sub_tree_1,sub_tree_2)
    # Exchange
    new_par_1 = deepcopy(par_1)
    offspring = replace_sub_tree(new_par_1, sub_tree_1,sub_tree_2)
    return offspring


# Mutation
def point_mutation(par, prob_mut_node):
    par_mut = deepcopy(par)
    prob = random()
    if prob < prob_mut_node:
	if isinstance(par_mut,ListType):
	    # Function
	    symbol = par_mut[0]
	    return [change_function(symbol)] + [point_mutation(arg, prob_mut_node) for arg in par_mut[1:]]
	elif isinstance(par_mut, (FloatType, IntType,LongType)):
	    # It's a constant
	    return change_constant()
	elif var_b(par_mut):
	    # It's a variable
	    return change_variable(par_mut)
	else:
	    raise TypeError # should not happen
    return par_mut


def change_function(symbol):
    new_function = choice(function_set)
    while (new_function[0] == symbol) or (new_function[1] != arity(symbol)):
	new_function = choice(function_set)
    return new_function[0]

def arity(symbol):
    for func in function_set:
	if func[0] == symbol:
	    return func[1]

def change_constant():
    return uniform(min_rnd, max_rnd)

def change_variable(variable):
    if len(vars_set) == 1:
	return variable
    new_var = choice(vars_set)
    while new_var == variable:
	new_var = choice(vars_set)
    return new_var




# Generate an individual: method full or grow
# FGGP: algorithm 2.1, pg.14
def gen_rnd_expr(func_set,term_set,max_depth,method):
	"""Generation of tree structures using full or grow."""
	if (max_depth == 0) or (method == 'grow'
	                        and (random() <
	                             (float(len(term_set)) / (len(term_set) + len(func_set))))):
		index = choice(range(len(term_set)))
		if index == (len(term_set) - 1) :
		    # ephemeral constant
		    ephemeral_const = term_set[index]
		    expr = eval(ephemeral_const)
		else:
		    # variable: 'Xn'
		    expr = term_set[index]
	else:
		func=choice(func_set)
		# func = [name_function, arity]
		expr = [func[0]] +  [gen_rnd_expr(func_set,term_set, max_depth -1, method)
		              for i in range(int(func[1]))]
	return expr


# If needed
def half_and_half(size):
	pop=[]
	for i in range(size/2):
		pop.append(gen_rnd_expr(func_set,term_set,3,'grow'))
	for i in range(size/2):
		pop.append(gen_rnd_expr(func_set,term_set,3,'full'))
	return pop

# Method ramped half-and-half.

def ramped_half_and_half(func_set,term_set,size, max_depth):
	depth=range(3,max_depth)
	pop=[]
	for i in range(size/2):
		pop.append(gen_rnd_expr(func_set,term_set,choice(depth),'grow'))
	for i in range(size/2):
		pop.append(gen_rnd_expr(func_set,term_set,choice(depth),'full'))
	return pop

# Parents' Selection

# Tournament
def tournament_selection(population,size):
    tam= len(population)
    mate_pool = []
    for i in range(tam):
	winner = tournament(population,size)
	mate_pool.append(winner)
    return mate_pool

def tournament_selection_b(population,size):
    return [tournament(population,size) for j in range(len(population))]

def tournament(population,size):
    """Maximization Problem.Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]


def tournament_negative(population,t_size):
    """Maximization Problem.Deterministic. Select the looser! Output index."""
    pop_size = len(population)
    pool_index = [choice(range(pop_size)) for j in range(t_size)]
    worst_index = pool_index[0]
    worst_indiv = population[worst_index]
    for i in range(1,t_size):
	if population[pool_index[i]][1] < worst_indiv[1]:
	    worst_index = pool_index[i]
	    worst_indiv = population[pool_index[i]]
    return worst_index

# Survivors' Selection

def survivors_elitism(parents,offspring,elite):
    """ Assume no size problems..."""
    size = len(parents)
    comp_elite = int(size * elite)
    new_population = parents[:comp_elite] + offspring[:size - comp_elite]
    return new_population

def survivors_generational(population,offspring):
    """Change all population with the new individuals."""
    return offspring


def survivors_steady_state(population,offspring,t_size):
    """
    Replace a bad individual with one from offspring.
    Population is dynamically updated!
    """
    for i in range(len(population)):
	looser = tournament_negative(population, t_size)
	population[looser] =offspring[i]
    return population


# Fitness Evaluation
def evaluate(individual,fit_cases):
    """
    Evaluate an individual. Gives the negative of the
    sum of the absolute error for each fitness cases.
    fit_cases = [[X1, ..., XN, Y], ...]
    """
    indiv = deepcopy(individual)
    error = 0
    for case in fit_cases:
        result = interpreter(indiv, case[:-1])
        error += abs(result - case[-1])
    return -error

# Interpreter. FGGP, algorithm 3.1 - pg.25
def interpreter(indiv,variables):
    if isinstance(indiv,ListType) :
        func = eval(indiv[0])
        if isinstance(func, FunctionType) and (len(indiv) > 1):
	    # Function: evaluate
            value = apply(func, [interpreter(arg,variables) for arg in indiv[1:]])
        else:
	    # Macro: don't evaluate arguments
            value = indiv
    elif isinstance(indiv, (FloatType, IntType,LongType)):
	# It's a constant
        value = indiv
    elif var_b(indiv):
	# It's a variable
        index = get_var_index(indiv)
        value = variables[index] # binding value
    elif isinstance(eval(indiv), FunctionType):
	# Terminal 0-ary function: execute
	value = apply(eval(indiv),())
    return value

def get_fit_cases(file_problem):
    f_in = open(file_problem,'r')
    data = f_in.readlines()
    f_in.close()
    fit_cases_str = [ case[:-1].split() for case in data[1:]]
    fit_cases = [[float(elem) for elem in case] for case in fit_cases_str]
    return fit_cases

def get_header(file_problem):
    f_in = open(file_problem)
    header_line = f_in.readline()[:-1]
    f_in.close()
    header_line = header_line.split()
    header = [eval(elem) for elem in header_line[:3]] + [[ [header_line[i], int(header_line[i+1])]
                                  for i in range(3,len(header_line),2)]]
    return header

def get_var_index(var):
    return int(var[1:])

def generate_vars(n):
    """ generate n vars, X1, ..., Xn."""
    vars_set = []
    for i in range(n):
        vars_set.append('X'+str(i))
    return vars_set

def var_b(name):
    """Test: is name a variable?"""
    return isinstance(name, StringType) and (name[0]== 'X') and (name[1:].isdigit())

def generate_var(prefix):
    count = 0
    while True:
        var_name = prefix + str(count)
        yield var_name
        count += 1

def indiv_size(indiv):
    """ Number of nodes of an individual."""
    if not isinstance(indiv, ListType):
        return 1
    else:
        return 1 + sum(map(indiv_size, indiv[1:]))


def run(num_runs,target,problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,elite_size,seed=0):
	# Colecta Dados
	print 'Wait, please '
	estatistica_total = [gp(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,elite_size,seed=0) for i in range(num_runs)]
	print "That's it!"
	# Processa Dados: melhor e médias por geração
	resultados_gera = zip(*estatistica_total)
	melhores = [max([indiv[0] for indiv in gera]) for gera in resultados_gera]
	medias = [sum([indiv[1] for indiv in gera])/float(num_runs) for gera in resultados_gera]
	# Mostra
	ylabel('Fitness')
	xlabel('Generation')
	titulo = 'Target: %s Runs: %d , Mutation: %0.2f, Xover: %0.2f' % (target,num_runs,prob_mut_node, prob_cross)
	title(titulo)
	p1 = plot(melhores,'r-o',label="Best")
	p2 = plot(medias,'g-s',label="Average")
	# Process Target
	# TODO
	legend(loc='lower right')
	show()


if __name__ == '__main__':
    count = 0
    run(3,'Simbolic Regression','data_symb.txt',30,40,6,10000,0.1,0.5,3,0.1,0)



