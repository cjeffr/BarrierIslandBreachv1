import numpy as np
import matplotlib.pyplot as plt
from clawpack.geoclaw import topotools
import os

file = os.path.join('/mnt/c/Projects/barrier_island/bathy/crm_vol1.nc')
topo = topotools.Topography()
topo.read(file)
topo.plot()
plt.show()