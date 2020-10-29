import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt

ax = plt.axes(projection = ccrs.Mercator())  # create a set of axes with Mercator projection
ax.add_feature(cf.COASTLINE)                 # plot some data on them
ax.set_title("Title")                        # label it
plt.show()