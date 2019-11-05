import os
import numpy as np
import matplotlib.pyplot as plt
path = os.path.join('c:/', 'fortranprograms', '_breach_patch')

breach_loc = os.path.join(path, 'breach_mesh')

b4_list = os.listdir(breach_loc)
# b4_array = np.zeros(shape=(len(b4_list), 2))
the_list = []

for l in b4_list:
    the_list.append(l.split('_'))
breach_array = np.array(the_list)
nx,dummy =np.shape(breach_array)
new_array = np.empty_like(breach_array)
for i in range(nx):
    dummy2 = breach_array[i,1]
    dummy1 = breach_array[i,0]
    dd2 = float(dummy2[0:-4])
    dd1 = float(dummy1)
    new_array[i,0] = dd1
    new_array[i,1] = dd2
    # print(i, breach_array[i,0],breach_array[i,1],new_array[i,0],new_array[i,1])
breach = new_array.astype('float')

for i in range(len(breach[:,0])):

    lon = breach[i,0]
    lat = breach[i,1]
    if (lon>=86.00) & (lon <=88.00) & (lat>25.0) & (lat < 26.0):
        print(lon, lat)

xx = np.linspace(-99,-70, 120)
yy = np.linspace(8,32, 120)
bb = np.linspace(-5000,0,120)
XX, YY = np.meshgrid(xx, yy)
_X, BB = np.meshgrid(xx, bb)
y_island = 25.6 # (m) location of the island up the shelf
h = 5 # (m) height at center of island
island_width = .2 # (m)
# width of the island's base in the ocean
beach_slope = 34/59e3 #slope 34 m of elevation over 59 km of distance
island_base = island_width/(np.cos(beach_slope))
bathymetry = BB
island_points = island_base/2
i0 = y_island - island_points
i1 = y_island + island_points
l1 = 2# (y >= i0)*(y<=i1)*np.ones(bathy.shape)*bathy
island = ( (YY < i0) * bathymetry +
         (YY >= i0) * (YY <= i1)*(np.ones(bathymetry.shape)*l1) +
         (YY > i1) * bathymetry)
plt.pcolor(XX, YY, island)
plt.xlim(-88, -85)
xtocks = np.linspace(-88.0, -85.0, 12)
xt = np.around(xtocks, 2)
plt.ylim(25.0,26.2)
plt.xticks(xt)
c = 0
colors = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'binary', 'spring']
for file in b4_list:
    fp = os.path.join(path, breach_loc, file)
    x = []
    y = []
    with open(fp) as f:
        print(f)
        data = np.loadtxt(f)
        xll = data[0]
        yll = data[1]
        mx = data[2]
        dx = data[4]
        dy = data[5]
        for i in range(int(dx)):
            x.append(xll + (i-0.5)*mx)
        for i in range(int(dy)):
            y.append(yll + (i-0.5)*mx)
        X, Y = np.meshgrid(x,y)
        b = np.ones(X.shape)
        plt.pcolormesh(X, Y, b, cmap=colors[c])
        c += 1

plt.show()




