# -*- coding: utf-8 -*-

import time
import datetime
import os
import sys
import matplotlib.pyplot as plt
import numpy as np


def timestamp():
    """Returns the current timestamp in a YYYYmmddHHMMSS format"""
    time_stamp = time.time()
    return datetime.datetime.fromtimestamp(time_stamp).strftime('%Y%m%d%H%M%S')


def init_project():
    """Verifies if the user as python version 3 and initializes the
    project directory."""
    if sys.version_info[0] < 3:
        print("This python project requires Python version 3.x")
        print("You could try:")
        print("source activate py3k")
        sys.exit(1)
    if not os.path.exists("out"):
        print("initializing project...")
        os.makedirs("out")
    if not os.path.exists("figures"):
        os.makedirs("figures")

# show results


def show(filename):
    """opens a file and plots in the matplotlib"""
    with open(filename, 'r') as f_data:
        data_1 = []
        data_2 = []
        data_3 = []
        for line in f_data:
            data = line[:-1].split(', ')
            data_1.append(str(data[0]))
            data_2.append(str(data[1]))
            data_3.append(str(data[2]))

    plt.grid(True)
    plt.title('Sum SubSet')
    plt.xlabel('Run')
    plt.ylabel('Best')
    plt.plot(data_1[1:], label=data_1[0])
    plt.plot(data_2[1:], label=data_2[0])
    plt.plot(data_3[1:], label=data_3[0])
    plt.legend(loc='upper left')
    plt.show()


def create_sample_test(dimension, limit):
    """creates a sample test of the max subset problem

    Keyword arguments:
    n -- the real part (default 0.0)
    limit -- the imaginary part (default 0.0)
    """
    lista = np.random.permutation(limit-1)
    lista = lista + 1
    return lista[:dimension]


if __name__ == '__main__':
    init_project()
    #print(timestamp())
    #a = create_sample_test(10,20)
    #print(a)
