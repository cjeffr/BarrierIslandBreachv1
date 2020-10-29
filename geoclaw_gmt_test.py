import os
from numpy import ma
from clawpack.pyclaw import Solution
import subprocess
import numpy as np
#
file_path = os.path.join('c:/', 'fortranprograms', 'plots', '_output')  #
# '''''/Users/jeffriesc/clawpack-5.4.1/geoclaw/examples/tsunami/TestingLinearity/SF_8_1m/_output'
solution = Solution()

drytol_default = .001
x = Solution(1, file_format='ascii')


for stateno, state in enumerate(x.states):
    # state = x.states[stateno]
    patch = state.patch
    level = patch.level
    print(stateno, patch.level)


    Xc, Yc = state.grid.c_centers
    xc = Xc[:,0]
    yc = Yc[0,:]
    h = state.q[0,:,:]
    eta = state.q[3,:,:]
    if (np.isnan(eta).any()) == True:

        print(np.isnan(eta).any())
    topo = eta - h
    # water = np.ma.masked_where(h <= drytol_default, eta)
    water = eta
    ind=np.where(h<=drytol_default)
    nan_index = np.where(eta <=.001)
    water[ind]=np.nan

    land = np.ma.masked_where(h > drytol_default, eta)
    #
    # output_file = 'test_{}.txt'.format(stateno)
    # with open(output_file, 'w') as f:
    #     for i in range(len(Xc)):
    #         for j in range(len(Xc.T)):
    #
    #             f.write('{} {} {}\n'.format(Xc[i,j], Yc[i,j], water[i,j]))
    # f.close()

