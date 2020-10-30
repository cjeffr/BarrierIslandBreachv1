import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

folders = ['reh10', 'reh20', 'reh30', 'reh40', 'reh50', 'reh75', 'reh100']
for i in range(0,20):
    for folder in folders:
        path = os.path.join('/mnt/c/RData/VT', 'rehoboth',f'{folder}', '_output') #"/Users/jeffriesc/Desktop/GF"


        # for j in range(140,141):
        file = open(os.path.join(path, "gauge{:05}.txt".format(i))) # %(i, j)), 'r')
        data = np.loadtxt(file)
        time = data[:,1]
        height = data[:,5]
        additional_increments = 1
        units_per_tick = 15
        seconds_per_increment = 15. * 60
        num_ticks = int(np.floor(max(time) / seconds_per_increment) + additional_increments)
        plt.figure('{}'.format(i) , figsize=(10, 10))
        plt.plot(time, height, label=folder)
        plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)
        # plt.xlim(-86400, 86400)
    plt.title('{}'.format(i))
    plt.legend()
    # plt.savefig(f'{i}.png')
    plt.show()

