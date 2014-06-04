# -*- coding: utf-8 -*-
from operator import itemgetter
import numpy
import matplotlib.pyplot as plt
import genetic_algorithm.survivors  as survivors
from copy import deepcopy

def init_runs_evaluation(generations, runs):
  #matrix with bests of each run per each
    bests_matrix = numpy.zeros(shape=(generations, runs))
    averages_matrix = numpy.zeros(shape=(generations, runs))
    return bests_matrix, averages_matrix


def evaluate_generation(population, bests_matrix, averages_matrix, current_generation, current_run):
    # Evaluate and sort
    #plot
    #new_population = deepcopy(population)
    avg_fit = generation_average_fit(population)
    best_fit = survivors.best_pop(population)[1]
    bests_matrix[current_generation][current_run] = best_fit
    averages_matrix[current_generation][current_run] = avg_fit



def generation_average_fit(population):
    sum_aux = sum([indiv[1] for indiv in population])
    return sum_aux/len(population)


def average_of_run_per_generation(averages_matrix):
    sumaux = numpy.sum(averages_matrix,axis=1)
    return sumaux/len(averages_matrix[0])


def best_of_run_per_generation(bests_matrix):
    maxs = numpy.max(bests_matrix,axis=1)
    return maxs


def final_evaluation(bests_matrix, averages_matrix):
    bests_per_generation = best_of_run_per_generation(bests_matrix)
    averages_per_generation = average_of_run_per_generation(averages_matrix)
    return bests_per_generation, averages_per_generation
    #plot


def test_function_represents_one_run_with_30_generations(bests_matrix, averages_matrix, max_gener, numb_runs,current_run):
    import init_pop
    import fitness
    sizes              = numpy.array([5, 8, 4, 11, 6, 12])
    max_size           = 20
    pop_size           = 10
    cromo_size         = len(sizes)
    fitness_func       = fitness.subset_fitness
    initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
    population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  #generation 1...30 generations
    for current_generation in range(max_gener):
        evaluate_generation(population, bests_matrix, averages_matrix,current_generation, current_run )
        # population is reinitialized to simulate that a generation changed
        initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
        population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)


def test_statistics_generates_case_sample_of_an_algorithm_with_30_generations_and_100_runs(bests_matrix, averages_matrix, max_gener, numb_runs):
    #simulate 100 runs
    for current_run in range(numb_runs):
        test_function_represents_one_run_with_30_generations(bests_matrix, averages_matrix, max_gener, numb_runs,current_run)



def save_statistics_and_create_graphs(
        time_stamp,
        bests_matrix_1, averages_matrix_1,
        bests_matrix_2, averages_matrix_2,
        bests_matrix_3, averages_matrix_3):
    bests_per_generation_1, averages_per_generation_1 = final_evaluation(bests_matrix_1, averages_matrix_1)
    bests_per_generation_2, averages_per_generation_2 = final_evaluation(bests_matrix_2, averages_matrix_2)
    bests_per_generation_3, averages_per_generation_3 = final_evaluation(bests_matrix_3, averages_matrix_3)

    figure_filename = 'figures/'+time_stamp+'.png'
    draw_graphic(figure_filename,bests_per_generation_1, averages_per_generation_1, bests_per_generation_2,
                        averages_per_generation_2,bests_per_generation_3, averages_per_generation_3)

    save_to_file(time_stamp, "bests", bests_per_generation_1,bests_per_generation_2,bests_per_generation_3)
    save_to_file(time_stamp, "averages", averages_per_generation_1,averages_per_generation_2,averages_per_generation_3)

    save_matrix(time_stamp, "bests_matrix_1", bests_matrix_1)
    save_matrix(time_stamp, "averages_matrix_1", averages_matrix_1)





def display_data(bests,averages, title):
    """Plot the data"""
    x1 = list(range(len(bests)))
    x2 = list(range(len(averages)))
    plt.grid(True)
    plt.title(title + ' - Sum SubSet')
    plt.xlabel('Run')
    plt.ylabel('Best')
    plt.plot(x1,bests, 'r')
    plt.plot(x2,averages, 'b')
    plt.show()

def draw_graphic(figure_filename,b1, a1, b2, a2,b3, a3):

    plt.grid(True)
    plt.figure(1)
    draw_subplot_generation_fitness(b1, a1, 221 , "First Case")
    draw_subplot_generation_fitness(b2, a2, 222 , "Second Case")
    draw_subplot_generation_fitness(b3, a3, 223, "Third Case")
    #plt.show()
    plt.savefig(figure_filename)


    pass

def draw_subplot_generation_fitness(bests, averages, position, title):
    x1 = list(range(len(bests)))
    x2 = list(range(len(averages)))
    plt.subplot(position)
    plt.title(title + ' - Sum SubSet')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(x1,bests, 'r')
    plt.plot(x2,averages, 'b')
    first_max_of_best_position = first_max_of_best(bests)
    center_of_sub_graph_position = center_of_sub_graph (bests, averages)
    anotate_first_max_of_bests(bests, first_max_of_best_position, center_of_sub_graph_position )
    pass

def anotate_first_max_of_bests(data, first_max_of_best_position, center_of_sub_graph_position):
    plt.annotate('first max'+str(first_max_of_best_position), xy=first_max_of_best_position, xytext=center_of_sub_graph_position,
        arrowprops=dict(facecolor='green', shrink=0.05),
        horizontalalignment='left',
        verticalalignment='bottom',
        bbox={'facecolor':'green', 'alpha':0.9, 'pad':10},
        color='white',)

def center_of_sub_graph(bests, averages):
    x = len(bests)/2
    ymin = numpy.min([bests, averages])
    ymax = numpy.max([bests, averages])
    y = ymin+ (ymax - ymin) / 2
    return (x, y)

def first_max_of_best(bests):
    #x = data.index(max(data))
    #y = max(data)
    y = numpy.max(bests)
    x = numpy.where(bests==y)[0][0]
    return (x, y)

def save_to_file(time_stamp, data_title, data1,data2,data3):
    with open('out/'+ time_stamp+'_'+data_title+'_generations('+str(len(data1))+').csv','w') as f_data:
        #header
        #f_data.write(data_title+'_case1,'+data_title+'_case2,'+data_title+'_case3\n')
        #body
        for i in range(len(data1)):
            f_data.write("%.0f" % data1[i] + ', ' + "%.0f" % data2[i]  + ', ' + "%.0f" % data3[i] + '\n')
        f_data.close()

def save_matrix(time_stamp, data_title, matrix):
    with open('out/'+ time_stamp+'_'+data_title+'_generations('+str(len(matrix))+').csv','w') as f_data:
        #header
        #f_data.write(data_title+'_case1,'+data_title+'_case2,'+data_title+'_case3\n')
        #body
        for line in matrix:
            for i in range(len(line)-1):
                f_data.write("%.0f" % line[i] + ', ')
            f_data.write("%.0f" % line[(len(line)-1)] + '\n')
        f_data.close()

if __name__ == '__main__':
    bests_matrix, averages_matrix = init_runs_evaluation(100,30)

    import utilities

    time_stamp         = utilities.timestamp()
    time_stamp = "111"
    max_gener = 100
    numb_runs = 30
    bests_matrix_1, averages_matrix_1 = init_runs_evaluation(max_gener,numb_runs)
    bests_matrix_2, averages_matrix_2 = init_runs_evaluation(max_gener,numb_runs)
    bests_matrix_3, averages_matrix_3 = init_runs_evaluation(max_gener,numb_runs)
    test_statistics_generates_case_sample_of_an_algorithm_with_30_generations_and_100_runs(bests_matrix_1, averages_matrix_1, max_gener, numb_runs)
    test_statistics_generates_case_sample_of_an_algorithm_with_30_generations_and_100_runs(bests_matrix_2, averages_matrix_2, max_gener, numb_runs)
    test_statistics_generates_case_sample_of_an_algorithm_with_30_generations_and_100_runs(bests_matrix_3, averages_matrix_3, max_gener, numb_runs)
    save_statistics_and_create_graphs(
        time_stamp,
        bests_matrix_1, averages_matrix_1,
        bests_matrix_2, averages_matrix_2,
        bests_matrix_3, averages_matrix_3)

   #print (runs_bests_1)
    #for i in range (0, 5):
    #  if runs_bests_1.find(i):
    #      print("cenas:"+i)



