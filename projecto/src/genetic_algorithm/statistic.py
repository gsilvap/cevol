# -*- coding: utf-8 -*-
from operator import itemgetter
import numpy
import matplotlib.pyplot as plt


def init_generation_evaluation():
    generations_bests = []
    generations_averages = []
    return generations_bests, generations_averages


def evaluate_generation(population, generations_bests, generations_averages):
    # Evaluate and sort
    population.sort(key=itemgetter(1), reverse = False) # Maximizing
    #plot
    best_fit = population[0][1]
    avg_fit =  generation_average_fit(population)
    generations_bests.append(best_fit)
    generations_averages.append(avg_fit)

def generation_average_fit(population):
    return sum([indiv[1] for indiv in population])/len(population)

def init_runs_evaluation():
  #matrix with bests of each run per each
    runs_bests = []
    runs_averages = []
    return runs_bests,runs_averages

def average_of_run_per_generation(runs_averages):
    sum = numpy.sum(runs_averages,axis=0)
    return sum/len(runs_averages)

def best_of_run_per_generation(runs_bests):
    maxs = numpy.max(runs_bests,axis=0)
    return maxs

def evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages ):
    #print ("generations_bests")
    #print (runs_averages)
    #print ("runs_bests")
    #print (runs_bests)
    runs_bests.append(generations_bests)
    runs_averages.append(generations_averages)

def final_evaluation(runs_bests, runs_averages):
    averages_per_generation = average_of_run_per_generation(runs_averages)
    bests_per_generation = best_of_run_per_generation(runs_bests)

    return bests_per_generation, averages_per_generation
  #plot
def test_function_represents_one_run_with_5_generations():
    generations_bests, generations_averages = init_generation_evaluation()
    import init_pop
    import fitness
    sizes              = numpy.array([5, 8, 4, 11, 6, 12])
    max_size           = 20
    pop_size           = 10
    cromo_size         = len(sizes)
    fitness_func       = fitness.subset_fitness
    initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
    population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

  #generation 1...5
    for i in range(5):
        evaluate_generation(population, generations_bests, generations_averages)
        # population is reinitialized to simulate that a generation changed
        initial_pop        = init_pop.init_pop(pop_size, cromo_size, init_pop.cromo_bin)
        population         = fitness.eval_pop(initial_pop, fitness_func, sizes, max_size)

    return generations_bests,generations_averages


def test_statistics_generates_case_sample_of_an_algorithm_with_5_generations_and_5_runs():
    runs_bests,runs_averages = init_runs_evaluation()
    #simulate 5 runs
    for i in range(5):
        generations_bests,generations_averages = test_function_represents_one_run_with_5_generations()
        evaluate_run(runs_bests, runs_averages, generations_bests, generations_averages)

    return runs_bests, runs_averages


def save_statistics_and_create_graphs(time_stamp, runs_bests_1, runs_averages_1, runs_bests_2, runs_averages_2,
                                                        runs_bests_3, runs_averages_3):
    bests_per_generation_1, averages_per_generation_1 = final_evaluation(runs_bests_1, runs_averages_1)
    bests_per_generation_2, averages_per_generation_2 = final_evaluation(runs_bests_2, runs_averages_2)
    bests_per_generation_3, averages_per_generation_3 = final_evaluation(runs_bests_3, runs_averages_3)

    figure_filename = 'figures/'+time_stamp+'.png'
    draw_graphic(figure_filename,bests_per_generation_1, averages_per_generation_1, bests_per_generation_2,
                        averages_per_generation_2,bests_per_generation_3, averages_per_generation_3)

    save_to_file(time_stamp, "bests", bests_per_generation_1,bests_per_generation_2,bests_per_generation_3)
    save_to_file(time_stamp, "averages", averages_per_generation_1,averages_per_generation_2,averages_per_generation_3)





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
        f_data.write(data_title+'_case1,'+data_title+'_case2,'+data_title+'_case3\n')
        #body
        for i in range(len(data1)):
            f_data.write("%.15f" % data1[i] + ', ' + "%.15f" % data2[i]  + ', ' + "%.15f" % data3[i] + '\n')
        f_data.close()



if __name__ == '__main__':
  global time_stamp
  import utilities

  time_stamp         = utilities.timestamp()

  runs_bests_1, runs_averages_1 = test_statistics_generates_case_sample_of_an_algorithm_with_5_generations_and_5_runs()
  runs_bests_2, runs_averages_2 = test_statistics_generates_case_sample_of_an_algorithm_with_5_generations_and_5_runs()
  runs_bests_3, runs_averages_3 = test_statistics_generates_case_sample_of_an_algorithm_with_5_generations_and_5_runs()
  save_statistics_and_create_graphs(time_stamp, runs_bests_1, runs_averages_1, runs_bests_2,
                                                        runs_averages_2, runs_bests_3, runs_averages_3)



