import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
from clawpack.geoclaw import topotools
import os

### Define the domain with a slope averaged from North Carolina shelf
beach_slope = 300 / 160  # slope 34 m of elevation over 160 km of distance
mx = 240

my = 10800

x = np.linspace(-94, -92, mx)
y = np.linspace(29.00, 30.0, my)
X, Y = np.meshgrid(x, y)
shelf_dy = .54829 #original bathy has y[29} == 29.54
cont_dy = 1 - shelf_dy #294/487.2
b_shelf = np.linspace(-101.5625, 0, (shelf_dy*my))
b_continent = np.linspace(0, 13.26, cont_dy*my+1)
b = np.append(b_shelf, b_continent)
X_d, B = np.meshgrid(x, b)

# Define island dimensions
idx = np.argmax(B >= -5, axis=0)
y_island = Y[idx[0]][0]  # (m) location of the island up the shelf
h = 5 # (m) height at center of island
island_width = .0045567  # (m)
# width of the island's base in the ocean
island_base = abs(island_width/(np.cos(beach_slope)))
bathymetry = B
island_points = island_base/2
i0 = y_island - island_points
i1 = y_island + island_points
l1 = 5


island = ( (Y < i0) * bathymetry +
             (Y >= i0) * (Y <= i1)*(np.ones(bathymetry.shape)*l1) +
             (Y > i1) * bathymetry) # *(X <= -80) + (X > -80)*bathymetry


# # Import geoclaw functions
# CLAW = os.environ['CLAW']

# create topography based on the simulated shelf
topo = topotools.Topography()
topo.x = x
topo.y = y
topo.Z = island
# generate the 2d grid and save the file
topo.generate_2d_coordinates()
topo.write(path="./island_1_3_arcsec.tt3", topo_type=3)
# fr = (-94.00, -92.0, 29.60, 32.00)
# topo2 = topo.crop(fr)
topo.plot()
plt.show()

# regions.append([7,7, ti, tf, -93.5, -92.5, 26.9, 27.1]):