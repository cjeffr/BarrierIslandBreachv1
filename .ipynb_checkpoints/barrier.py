import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.io import FortranFile

# Define the domain with a slope averaged from North Carolina shelf
beach_slope = 500/600e3 # slope 34 m of elevation over 59 km of distance
b0 = -600  # y intercept where water and beach meet
h0 = -.22  # (m) at y=0
mx = 3480
my = 2880

x = np.linspace(-99, -70, mx)

y = np.linspace(8, 32, my)
Y, X = np.meshgrid(x, y)
b = np.linspace(-5000, 0, my)
B, _X = np.meshgrid(b, x)


plt.figure(121)
plt.pcolor(X, Y, B)
# Define island dimensions
y_island = 25.6  # (m) location of the island up the shelf
h = 5  # (m) height at center of island
island_width = .2  # (m)
# width of the island's base in the ocean
island_base = island_width/(np.cos(beach_slope))
bathymetry = B
island_points = island_base/2
i0 = y_island - island_points
i1 = y_island + island_points
l1 = 2  # (y >= i0)*(y<=i1)*np.ones(bathy.shape)*bathy
island = ((Y < i0) * bathymetry +
          (Y >= i0) * (Y <= i1)*(np.ones(bathymetry.shape)*l1) +
          (Y > i1) * bathymetry)
plt.figure()
plt.subplot(121)
plt.pcolor(X, Y, bathymetry)
plt.subplot(122)
plt.pcolor(X, Y, island)
plt.show()
# fig, ax = plt.subplots()
time = np.linspace(0.0, 10.0, 10)

t1 = 3.0
t2 = 6.0
A_max = 5.0
A1 = ((time < t1) * np.zeros(time.shape)
      + (t1 <= time) * (time < t2) * (A_max / (t2-t1) * (time - t1))
      + (t2 <= time) * np.ones(time.shape) * A_max)
A2 = .2*y
sigma = 1.0
h0 = 10
x1 = -88.0
x2 = -86.0
y1 = 25.5
y2 = 25.7
mu = -87.0
# ?\plt.figure()
breach = island
# for i in range(len(A1)):

# amplitude affects the gradation of the breach
breach -= (5 * np.exp((-1/2)*(X - mu)**2 / sigma**2) * (x1 <= X) * (X <= x2) * (y1 <= Y)*(Y <= y2) * (0.25 * breach))
#     plt.clf()
# breach = breach - (500  * np.exp(-X**2 / sigma**2)* (x1 <= X) * (X <= x2) * (y1 <= Y)*(Y<= y2)) #(0.10 * Y)
#
plt.figure()
plt.pcolor(X, Y, breach)
plt.ylim(25, 26)
plt.colorbar()
plt.clim(-5, 5)
plt.show()