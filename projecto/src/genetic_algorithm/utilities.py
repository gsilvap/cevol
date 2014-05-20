# -*- coding: utf-8 -*-

import time
import datetime
import os
import errno
import sys
import matplotlib.pyplot as plt



def timestamp():
  ts = time.time()
  return datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

def init_project():
  if sys.version_info[0] < 3:
    print("This python project requires Python version 3.x")
    print("You could try:")
    print("source activate py3k")
    sys.exit(1)
  if not os.path.exists("out"):
    print ("initializing project...")
    os.makedirs("out")

# show results
def show(filename):
  with open(filename,'r') as f_data:
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
    plt.plot(data_2[1:],label=data_2[0])
    plt.plot(data_3[1:],label=data_3[0])
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
  init_project()
  print(timestamp())

