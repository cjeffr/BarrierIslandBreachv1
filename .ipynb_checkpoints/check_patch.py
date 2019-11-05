import os
import numpy as np



path = os.path.join('c:/', 'fortranprograms', '_breach_patch')

b4_loc = os.path.join(path, 'b4step_mesh')
breach_loc = os.path.join(path, 'breach_mesh')

b4_list = os.listdir(b4_loc)
# b4_array = np.zeros(shape=(len(b4_list), 2))
the_list = []

for l in b4_list:
    the_list.append(l.split('_'))
b4_array = np.array(the_list)
nx,dummy =np.shape(b4_array)
new_array = np.empty_like(b4_array)
for i in range(nx):
    dummy2 = b4_array[i,1]
    dummy1 = b4_array[i,0]
    dd2 = float(dummy2[0:-4])
    dd1 = float(dummy1)
    new_array[i,0] = dd1
    new_array[i,1] = dd2
    print(i, b4_array[i,0],b4_array[i,1],new_array[i,0],new_array[i,1])
b4 = new_array.astype('float')

for i in range(len(b4[:,0])):

    lon = b4[i,0]
    lat = b4[i,1]
    if (lon>=86.00) & (lon <=88.00) & (lat>25.0) & (lat < 26.0):
        print(lon, lat)










