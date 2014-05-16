import time
import datetime
import os
import errno
import sys



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

if __name__ == '__main__':
  init_project()
  print(timestamp())
