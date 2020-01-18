import numpy as np
import matplotlib.pyplot as plt
from clawpack.geoclaw import topotools
import os

file = os.path.join('/mnt/c/RData/Seaside/Bathy/Cascadia_island1.tt3')
topo = topotools.Topography()
topo.read(file)
topo.plot()
plt.show()