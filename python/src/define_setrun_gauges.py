import os
import numpy as np
"""
Creates a text file for the setrun needed gauge locations, evenly spaces each gauge between the breach end points
depending on how many gauges are required
"""
path = '/mnt/c/fortranprograms/'
lat0 = 29.51
lat1 = 29.535
lon0 = -94.5
lon1 = -94.0
num_gauges = 20

file = os.path.join(path, 'ocean.txt')
with open(file, 'w') as f:
    # for i in range(0,20):
    for i in range(num_gauges):
        lon = lon0 - i*(lon0 - lon1)/num_gauges
        # lon = lon0 - (i)*(lon0 - lon1)/20
        f.write(f'rundata.gaugedata.gauges.append([{i}, {lon}, {lat0}, ti, tf])\n')
f.close()
file = os.path.join(path, 'bay.txt')
with open(file, 'w') as f:
    # for i in range(0,20):
    for i in range(num_gauges, num_gauges*2):
        lon = lon0 - (i-num_gauges)*(lon0 - lon1)/num_gauges
        # lon = lon0 - (i)*(lon0 - lon1)/20
        f.write(f'rundata.gaugedata.gauges.append([{i}, {lon}, {lat1}, ti, tf])\n')
f.close()