import os
import numpy as np
import matplotlib.pyplot as plt

path = os.path.join('c:/', 'fortranprograms', '_b_', '_output')
file = os.path.join(path, 'gauge00021.txt')

data = np.loadtxt(file)

refinement = data[:,0]
np.min(refinement)