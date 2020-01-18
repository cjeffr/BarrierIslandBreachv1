from clawpack.geoclaw import topotools
import os
import numpy as np
import matplotlib.pyplot as plt

topo = topotools.Topography()

def read_bathy(file, topo):
    """

    :param file: bathymetry file name/path
    :return:
    """
    topo.read(file, topo_type=3)
    print("The extent of the data in longitude and latitude: ", topo.extent)
    print("The shapes of 1-dimensional arrays of longitude x and latitude y values:", topo.x.shape, topo.y.shape)
    print("The shapes of 2-dimensional arrays X,Y and the topography data Z:", topo.Z.shape)
    print("topo.delta = ", topo.delta)
    print("3 arcminutes is 1/20 degree = %8.6f degree" % (1. / 6.))
    return topo

# \bathy = os.path.join('/mnt/c/', 'RData', 'Bathy',  'NA_CAS_pixel.asc')
# read_bathy(bathy, topo)

def add_barrier(topo, bathy):
    """
    :param bathy: bathymetry file name/path
    :return:
    """

    # Pre-defined variables
    X = topo.X
    Y = topo.Y
    B = topo.Z
    rise = abs(topo.Z[0][0] - topo.Z[0][-1])
    run = abs(topo.X[0][0] - topo.X[0][-1])
    slope = rise / run

    # User Defined variables
    height = 3
    island_loc = -123.98
    island_width = .009
    lat0 = 45.94
    lat1 = 46.17

    # Calculations for begin and end of island
    island_base = abs(island_width/(np.cos(slope)))
    island_points = island_base/2
    i0 = island_loc - island_points
    i1 = island_loc + island_points
    # If the bathymetry is inside the range of l1 and l0 alter it to place an island
    # if the bathymetry is outside that range, ensure it is just copied from the original data
    island = ((X < i0) * B + (X >= i0) * (X <= i1)*(np.ones(B.shape)*height) +
              (X > i1) * B) * (Y >= lat0)*(Y <= lat1) + (Y < lat0)*B + (Y > lat1)*B
    return X, Y, island

def plot_island(X, Y, island, topo):
    """

    :param X:
    :param Y:
    :param island:
    :return:
    """
    plt.pcolor(X, Y, island, vmin=-10, vmax=5)
    # if you want to zoom in on a location in the plot
    # plt.xlim(-124.3, -123.6)
    # plt.ylim(45.5, 46.2)
    plt.show()

    # Compare with geoclaw's defined output
    topo.generate_2d_coordinates()
    topo.plot()
    plt.show()
    # To Crop the region
    filter_region = (-124.0399537037037, -123.89060185184958, 45.9000462962963, 46.1790277777805)
    topos = topo.crop(filter_region)
    topos.plot()
    plt.show()


def write_topo(topo):
    write_path = './Cascadia_island_3m.tt3'
    topo.write(path=write_path, topo_type=3)


def sim_breach(X, Y, island):
    """

    :param X: Longitude matrix
    :param Y: latitide maxtrix
    :param island: bathymetry depth matrix
    :return:
    :x1, x2, y1, y2: location of breach in lat/lon
    :breach_timing: numeber of time steps for breaching to occur
    :sigma: breach width variance
    :mu: location of center of breach
    :amp: amplitude of breach depth change per timestep
    :tr: timing ratio of breach
    """
    sigma = 1

    x1 = -123.99
    x2 = -123.97
    y1 = 46.03
    y2 = 46.05
    mu = 46.04
    breach = island
    breach_timing = 5
    amp = 1.0
    tr = 0.65
    for i in range(len(breach_timing)):
        breach = breach - (amp * np.exp((-0.5)*(Y-mu)**2 / sigma**2) * (tr * breach) * (x1 <= X)
                           * (X <= x2) * (Y >= y1) * (Y <= y2))
        plt.figure()
        plt.pcolor(X, Y, breach, vmin=0.00, vmax=5.0)
        plt.colorbar()
        plt.ylim(45.90, 46.2)
        plt.xlim(-124.03, -123.89)
        plt.show()
