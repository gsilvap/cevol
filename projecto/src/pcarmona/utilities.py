import time
import datetime
import os
import errno

def timestamp():
  ts = time.time()
  return datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

def init_project():
  if not os.path.exists("out"):
    print "initializing project..."
    os.makedirs("out")

if __name__ == '__main__':
  init_project()
  print(timestamp())
