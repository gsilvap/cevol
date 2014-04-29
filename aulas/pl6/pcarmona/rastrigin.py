from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

def rastrigin():

  fig = plt.figure()

  fig.suptitle('Rastrigin', fontsize=18, fontweight='bold')

  ax = Axes3D(fig)

  X = np.arange(-5.12, 5.12, 0.1)

  Y = np.arange(-5.12, 5.12, 0.1)

  X, Y = np.meshgrid(X, Y)
  Z = 10*(X**2 - 10* np.cos(2*3.14159*X)) + 10*(Y**2 - 10* np.cos(2*3.14159*Y))
  ax.plot_surface(X, Y, Z, rstride=1,cstride=1,cmap=cm.jet)
  ax.legend()
  plt.show()

if __name__ == '__main__':
  rastrigin()
