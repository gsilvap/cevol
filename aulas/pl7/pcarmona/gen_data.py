#! /usr/bin/env ptython
# -*- coding: utf-8 -*-
"""
Data generation for GP.
Ernesto Costa, March 2012
Revised for Python 3 in March 2014
gen_data.py
"""

import matplotlib.pyplot as plt
from math import sin, pi


def data_creation(file_name,function,domain,numb_cases,*function_set):
    """
    domain = [...,(inf, sup),...], inf = starting value, sup = end value
    function_set = (...,(name_function, arity), ...)
    """
    f_out = open(file_name,'w')
    # Header
    header_base = str(len(domain)) + '\t'
    header = header_base + ''.join([function_set[i][0] +'\t'+str(function_set[i][1])+'\t' for i in range(len(function_set))])[:-1] + '\n'
    f_out.write(header)

    # generate fitness cases
    cases = []
    for i in range(len(domain)):
        init = domain[i][0]
        end = domain[i][1]
        step = (end - init) / numb_cases
        cases.append(list(frange(init,end,step)))
    inputs = list(zip(*cases))
    print(inputs)
    outputs = [function(*in_vector) for in_vector in inputs]
    # save to file
    for i in range(numb_cases):
        line = ''.join([str(val) + '\t' for val in inputs[i]]) + str(outputs[i]) + '\n'
        f_out.write(line)
    f_out.close()


def plot_data(file_name, name,body,loc):
    f_in = open(file_name)
    # read fitness cases
    data = f_in.readlines()[1:]
    f_in.close()
    # plot
    values_x = [float(line[:-1].split()[0]) for line in data]
    values_y = [float(line[:-1].split()[-1]) for line in data]
    plt.ylabel('Value')
    plt.xlabel('Input Values')
    plt.title(name)
    p = plt.plot(values_x,values_y,'r-o',label=str(body))
    plt.legend(loc= loc)
    plt.show()


def simbolic_regression_2(x):
    return x**2 + x + 1

def sphere(x,y):
    return x**2 + y**2

def sin_w(x):
    return sin(x)


def frange(start,stop,step):
    value = start
    while value < stop:
        yield value
        value += step



if __name__ == '__main__':

    # First Set
    data_creation('data_sin.txt',sin,[(-3.14, 3.14)], 62, ('add_w',2),('sub_w',2), ('mult_w',2),('div_prot_w',2))
    plot_data('data_sin.txt','sin', 'sin(x)', 'upper right')

    # Second Set
    data_creation('data_symb.txt',simbolic_regression_2,[(-1.0, 1.0)], 21, ('add_w',2),('sub_w',2), ('mult_w',2),('div_prot_w',2))
    plot_data('data_symb.txt','Symbolic Regression','x**2 + x + 1','lower right')

    # Third set
    data_creation('data_sphere.txt',sphere,[[-5,5],[-5,5]], 22, ('add_w',2),('sub_w',2), ('mult_w',2),('div_prot_w',2))
    plot_data('data_sphere.txt','Sphere','X**2 + Y**2', 'upper right')





