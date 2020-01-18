import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from clawpack.geoclaw import topotools

def fake_bathy(grid_resolution, degrees_x, degrees_y, xlow, ylow):
    """
    Define the domain with a slope averaged from North Carolina shelf
    :param grid_resolution:
    :param degrees_x:
    :param degrees_y:
    :param xlow:
    :param ylow:
    :return:
    """
    sec_per_degree = 3600  # 60 minutes per degree * 60 seconds per  minute
    mx = degrees_x * sec_per_degree / grid_resolution  # for 30 arcseconds @ 29 degrees = 3480
    my = degrees_y * sec_per_degree / grid_resolution  # for 30 arcseconds @ 12 degrees = 1440
    # define change in depth per North Carolina shelf/gulf of mexico
    mb_shelf = (1.61/degrees_y) * my  # 1.61*3600/30 # 1.61 degrees converted to 30 arcseconds
    mb_cont = (2.45/degrees_y) * my  # 3600/30 # 2.45 degrees converted to 30 arc seconds
    mb_steep = (2.02/degrees_y) * my  # *3600/30
    mb_deep = (5.92/degrees_y) * my  # *3600/30
    x = np.linspace(xlow, xlow + degrees_x, mx)
    y = np.linspace(ylow, ylow + degrees_y, my)

    b_deep = np.linspace(-5000, -2500, mb_deep+1)
    b_steep = np.linspace(-2500, -300, mb_steep)
    b_shelf = np.linspace(-300, 0, mb_shelf)
    b_continent = np.linspace(0, 72, mb_cont)
    b = np.append(b_deep, b_steep)
    b = np.append(b, b_shelf)
    b = np.append(b, b_continent)

    X, Y = np.meshgrid(x, y)
    _X_d, B = np.meshgrid(x, b)
    return X, Y, B, mx, my
def create_island(X, Y, B, mx, my):

    # Define island dimensions
    beach_slope = 300 / 160  # slope 34 m of elevation over 160 km of distance
    idx = np.argmax(B >= -5, axis=0)
    y_island = Y[idx[0]][0]  # (m) location of the island up the shelf
    h = 5  # (m) height at center of island
    island_width = .0045567  # (degrees)
    # width of the island's base in the ocean
    island_base = abs(island_width/(np.cos(beach_slope)))
    bathymetry = B
    island_points = island_base/2
    i0 = y_island - island_points
    i1 = y_island + island_points

    island = ((Y < i0) * bathymetry + (Y >= i0) * (Y <= i1)*(np.ones(bathymetry.shape)*h) +
              (Y > i1) * bathymetry) *(X >= -90)*(X <= -80) + (X < -90)*bathymetry + (X > -80)*bathymetry
    plt.figure()
    plt.pcolor(X, Y, island, vmin=-10, vmax=5)
    plt.colorbar()
    plt.show()

    for i in range(my):
        for j in range(mx):
            if island[i, j] == h and (island[i, j-1] < 4):
                # print(i, j,'land')
                if island[i+1, j-1] < 5:
                    land_y = i
                    land_x = j - 1
                    while island[land_y, land_x] < 5:
                        print(land_x, land_y)
                        for k in range(-65, 40):  # this is dangerous, if we were at x < 62 it will crash
                            #     # for l in range(3):
                            print(k)
                            island[land_y + 1, land_x - k] = h
                        land_y += 1
                        land_x -= 1
                        print(land_y, land_x,'not land')
    for i in range(my):
        for j in range(mx):
            if X[i, j] >= -80:
                if island[i, j] == h and (island[i, j+1] < 4):
                # print(i, j,'land')
                    if (island[i+1, j+1] < 5) :
                        land_y = i
                        land_x = j + 1
                        while island[land_y, land_x] < 5:
                            print(land_x, land_y)
                            for k in range(-65, 40):  # this is dangerous, if we were at x < 62 it will crash
                                #     # for l in range(3):
                                print(k)
                                island[land_y + 1, land_x + k] = h
                            land_y += 1
                            land_x += 1
                            print(land_y, land_x,'not land')

    plt.figure()
    plt.pcolor(X, Y, island, vmin=-10, vmax=5)
    plt.ylim(29, 30)
    plt.colorbar()
    plt.show()
    return X, Y, island
def create_fake_topo(X, Y, island, bathy_name):
    topo = topotools.Topography()
    # create topography based on the simulated shelf
    x = X[0]
    y = Y[0]
    topo = topotools.Topography()
    topo.x = x
    topo.y = y
    topo.Z = island
    # generate the 2d grid and save the file
    topo.generate_2d_coordinates()
    topo.write(path=bathy_name, topo_type=3)
