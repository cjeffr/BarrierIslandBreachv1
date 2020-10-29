from clawpack.pyclaw import Solution
import os
import xarray as xr
import pandas as pd
import numpy as np


def read_fortq(frame):
    """
    Import fort.q files to get x,y,z data
    """
    fortq = Solution(frame, file_format='ascii')
    patch_dict = {}
    for stateno, state in enumerate(fortq.states):
        patch = state.patch
        level = patch.level
        Xc, Yc = state.grid.c_centers
        h = state.q[0, :, :]
        eta = state.q[3, :, :]
        drytol_default = 0.001
        water = np.copy(eta)
        idx = np.where((h <= drytol_default) & (h >= -drytol_default))
        water[idx] = np.nan
        #         idx2 = np.where(eta==0)
        #         water[idx2] = np.nan

        # Save variables to dictionary
        long = Xc[:, 0]
        lat = Yc[0]
        patch_dict[stateno] = {"lat": lat, 'long': long, 'eta': eta, 'amr_level': level, 'Xc': Xc, 'Yc': Yc,
                               'water': water}
    return patch_dict, water, h, Xc, Yc, eta
[patch_dict, water, h, X, Y, eta]=read_fortq(4)