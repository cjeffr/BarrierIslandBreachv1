import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

### Define the domain with a slope averaged from North Carolina shelf
beach_slope = 500 / 600e3  # slope 34 m of elevation over 59 km of distance
b0 = -600  # y intercept where water and beach meet
h0 = -.22  # (m) at y=0
mx = 193

my = 160

x = np.linspace(-99, -70, mx)
y = np.linspace(8, 32, my)
X, Y = np.meshgrid(x, y)
b = np.linspace(-1000, 200, my)
X_d, B = np.meshgrid(x, b)

# Define island dimensions
y_island = 27.00 # (m) location of the island up the shelf
h = 2 # (m) height at center of island
island_width = .072 # (m)
# width of the island's base in the ocean
island_base = island_width/(np.cos(beach_slope))
bathymetry = B
island_points = island_base/2
i0 = y_island - island_points
i1 = y_island + island_points
l1 = 2

island = ( (Y < i0) * bathymetry +
             (Y >= i0) * (Y <= i1)*(np.ones(bathymetry.shape)*l1) +
             (Y > i1) * bathymetry)*(X <= -80) + (X > -80)*bathymetry
plt.figure()
plt.pcolor(X, Y, island,norm=colors.Normalize(vmin=-10, vmax=2))



plt.colorbar()

plt.show()


for i in range(my):
    for j in range(mx):
        if island[i,j] == 2 and (island[i, j+1] < 0):
            # print(i,j,'land')
            if (island[i+1, j+1] < 0) :
                land_y = i
                land_x = j + 1
                while island[land_y, land_x] < 2:
                    # print(land_x, land_y)
                    for k in range(-10, 10):  # this is dangerous, if we were at x < 62 it will crash
                        #     # for l in range(3):
                        island[land_y + 1, land_x + k] = 2
                    land_y += 1
                    land_x += 1
                # print(i+1, j+1,'not land')
                # for k in range(-62,62):
                #     # print('not land: making updates')
                #     island[i + 1, j + k] = 2

                    # island[i + 1, j] = 2
                # island[i + 1, j + 2] = 2
                # if island[i,j-1] == 2:
                #     island[i+1, j+1] = 2

stuff = np.where(island == 2)
coords = list(zip(stuff[0], stuff[1]))
# plt.figure()
# # plt.pcolor(X, Y, island,vmin=-10, vmax=2)
#
#
# plt.colorbar()


# plt.ylim(27.0, 28.5)
# plt.xlim(-80.2, -79.2)
plt.show()
width = 3
height = [3,2,1,0]
breach = island.copy()
breach_loc = (-90, 27)
for i in range(4):
    for xidx, j in enumerate(x):
        for yidx, k in enumerate(y):
            if (j <= -90.) and (j >= -91.0):
                if (k >= 27) and (k <= 27.2):
                    print(breach[yidx, xidx])
                    # print('found something')
                    # print(j)
                    b = (j+90.5)**2 + i
                    print(b)
                    breach[yidx, xidx] = breach[yidx, xidx] - b
                    print(breach[yidx, xidx])
    # breach = breach -
    plt.pcolor(X,Y,breach, norm=colors.Normalize(vmin=0, vmax=2))
    plt.ylim(26, 28)
    plt.savefig(f'/mnt/c/Projects/plots/{i}.png')
    plt.show()

# # loc = plticker.MultipleLocator(base=0.1) # this locator puts ticks at regular intervals
# # plt.yaxis.set_major_locator(loc)
# plt.show()
#
#
# time = np.linspace(0.0, 10.0, 10)
# # y = np.linspace(0.0, 60e3, 600)
# # x = np.linspace(-100, -10, 500)
# # b = np.linspace(-600, 0, 600)
# # X, Y = np.meshgrid(x, y)
# # X_B, B = np.meshgrid(x, b)
# XX = X
# YY = Y
# t1 = 3.0
# t2 = 6.0
# A_max = 5.0
# A1 = (  (time < t1) * np.zeros(time.shape)
#       + (t1 <= time) * (time < t2) * (A_max / (t2-t1) * (time - t1))
#       + (t2 <= time) * np.ones(time.shape) * A_max)
# A2 = .2*y
# sigma = 1.0
#
# h0 = 10
# x1 = -88.
# x2 = -86.
# y1 = 30.60
# y2 = 30.70
# mu = 1.0
# # plt.pcolor(X, Y, B)
# # plt.show()
# breach = island #np.ones(X.shape) * 27.
# for i in range(len(A1)):
#     breach = breach - ( 1.0* np.exp((-0.5)*(X+87.)**2 / sigma**2) * (0.25 * breach)  * (x1 <= X) * (X <= x2) * (Y >=y1)*(Y<=y2))
# #     plt.clf() (sigma*np.sqrt(2*np.pi))
#     plt.figure()
#     plt.pcolor(XX, YY, breach, vmin=0.00, vmax=5.0)
#     plt.colorbar()
#     plt.ylim(28.0,32.0)
#     plt.show()