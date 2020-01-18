""""
This code takes the un-altered green's functions and slip, multiplies each slip value to the
appropriate subfault number to get the correct amount of slip per subfault and then sums each
waveform for each site (gauge location) and passes one array rather than 200 back to the
rest of the program.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import ticker
import matplotlib.gridspec as gridspec
from matplotlib import rcParams


def create_subplot(nrows, ncols, index):

    fig = plt.figure(1,figsize=(18, 6))
    gs = gridspec.GridSpec(nrows, ncols,  width_ratios=[3,3,3], height_ratios=[.5,.5,.5])
    gs.update(hspace=0.0, wspace=0.15)
    ax = plt.subplot(gs[index]) # nrows, ncols, index
    return fig, ax

def no_cols(ar_len):

    if ar_len % 2 ==0:
        nrows = ar_len / 2
        ncols = ar_len / 2
    elif ar_len % 3 == 0:
         nrows = ar_len / 3
         ncols = ar_len / 3
    else:
        nrows = ar_len
        ncols = 1
    return(nrows, ncols)

def create_group_plot(ar_len, i, v, gauges, wave, time_interval, g, eq_time, nrows, ncols):
    index = i + 1
    fig, ax = create_subplot(nrows, ncols, i)

    # Make the plot pretty
    # X ticks
    additional_increments = 1
    units_per_tick = 30
    seconds_per_increment = 30. * 60
    num_ticks = int(np.floor(max(time) / seconds_per_increment) + additional_increments)

    # Y Ticks
    tick_units = 0.5
    m_per_increment = 0.5
    y_num_ticks = int(np.floor(max(wave[:,v]) / m_per_increment) + additional_increments)

    # removing data points = 0 for tide gauges that were destroyed
    miy = np.nonzero(g[:, 4])
    ofu = np.nonzero(g[:, 5])
    ayu = np.nonzero(g[:, 6])

    # Actual plot items

    if v == 4:
        ax.plot(time_interval, wave[:, v], 'b', label='Modeled')
        ax.plot(eq_time[:, v][miy], g[:, v][miy], 'r', label='Measured')

    elif v == 5:
        ax.plot(time_interval, wave[:, v], 'b', label='Modeled')
        ax.plot(eq_time[:, v][ofu], g[:, v][ofu], 'r', label='Measured')

    elif v == 6:
        ax.plot(time_interval, wave[:, v], 'b', label='Modeled')
        ax.plot(eq_time[:, v][ayu], g[:, v][ayu], 'r', label='Measured')
    elif v == 18:
        file = os.path.join('c:/Rdata','Japan', 'GaugeFiles', '21413_no_tide.txt')
        dart = np.loadtxt(file)
        ax.plot(time_interval, wave[:, 18], 'b', label='Modeled')
        ax.plot(dart[:, 0], dart[:, 1], 'r', label='Measured')
    elif v == 19:
        file = os.path.join('c:/Rdata','Japan', 'GaugeFiles', '21418_no_tide.txt')
        dart = np.loadtxt(file)
        ax.plot(time_interval, wave[:, 19], 'b', label='Modeled')
        ax.plot(dart[:, 0], dart[:, 1], 'r', label='Measured')
    else:
        ax.plot(time_interval, wave[:, v], 'b', label='Modeled')
        ax.plot(eq_time[:, v], g[:, v], 'r', label='Measured')
    plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)

    if index < (ar_len - 2):
        plt.xticks([])
    else:
        plt.xticks([seconds_per_increment * i for i in range(num_ticks)],
                   ['%d' % (i * units_per_tick) for i in range(num_ticks)])
    # This is for Shao ticks
    plt.yticks(np.arange(min(wave[:,v]), max(wave[:,v]), 4.0))

    locator = ticker.MaxNLocator(nbins=5)
    plt.gca().yaxis.set_major_locator(locator)
    ax.title.set_position([0.5, .83])
    # This is for GNSS ticks

    # max_y = np.max(g[:, v]) + 0.5
    # min_y = np.min(g[:, v]) - 1.0
    # ax.set_ylim([min_y, max_y])
    # yticks = ticker.MaxNLocator(3)
    # plt.yticks(yticks)

    plt.xlim(0, 14400.)
    handles, labels = ax.get_legend_handles_labels()
    plt.figlegend(handles, labels, loc='upper right', prop={'size': 12})
    if str(gauges[v][0]) in ['21418', '21413']:
        plt.title('DART {} '.format(str(gauges[v][0])))
    else:
        plt.title('{} Tide Gauge'.format(str(gauges[v][0])))

    plt.tick_params(labelsize=12)
    return fig

def plot_gauges(gauges_no, wave, time_interval, compare, eq_time):

    print('len gauges = ', len(wave))
    fig =  plt.figure()

    plt.subplots_adjust(hspace=0.000)
    plt.gca().yaxis.set_minor_formatter(ticker.NullFormatter())


    # loop = np.arange(0,9) #[18, 19, 1, 4, 5, 6, 7, 8, 9, ]

    # Make the plot pretty
    # X ticks
    additional_increments = 1
    units_per_tick = 30
    seconds_per_increment = 30. * 60
    num_ticks = int(np.floor(max(eq_time) / seconds_per_increment) + additional_increments)

    plt.plot(eq_time,compare, 'k--', label='No Breach')


    plt.plot(time_interval, wave, 'r', label='Breach')

    plt.title('Gauge {}'.format(gauges_no))
    plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)

    plt.xlabel("Time (minutes)", fontsize=16)  # declare the x axis label
    plt.ylabel("Wave Amplitude (m)", fontsize=16)
    plt.xticks([seconds_per_increment * i for i in range(num_ticks)],
               ['%d' % (i * units_per_tick) for i in range(num_ticks)])
    plt.legend(loc='upper right')
    plt.savefig('SeasideGaugeNumber {}.png'.format(gauges_no))
    plt.show()
    # plt.savefig('{}.png'.format(wave[0][0]))


sgf_path = '/mnt/c/seaside/'
# sims = ['breach', 1, 2, 3, 4, 5, 6, 7, 8, 9]
gauges = [2, 4, 6, 8, 10, 12, 14,15,16, 17, 18, 24, 26, 28, 30, 32, 34, 35, 36, 37]
for g in gauges:

    compare = os.path.join('/mnt/c/seaside/3m/no_b3m/_output', 'gauge{:05d}.txt'.format(g))
    compare_data = np.genfromtxt(compare, usecols=5, dtype='float')
    compare_time = np.genfromtxt(compare, usecols=1, dtype='float')

    gauge_file = os.path.join(sgf_path, 'redo1/', 'gauge{:05d}.txt'.format(g))

    times = np.genfromtxt(gauge_file, usecols=1, dtype='float')
    data = np.genfromtxt(gauge_file, usecols=5,  dtype='float')
    # gauge_data.append((g, times, data))
    # time_data.append(times)
# print(len(gauge_data))
    plot_gauges(g, data, times, compare_data, compare_time)
#
# gauges = []
# for i in range(len(gauge_no)):
#     station, no = (gauge_name[i], gauge_no[i])
#
#     gauges.append((station, no))
#
# eq_path = os.path.join('c:/','RData','Japan', 'GaugeFiles')
#
# loop = [18, 19, 1, 4, 5, 6, 7, 8, 9, ]
# ar_len = len(loop)
# ncols, nrows = no_cols(ar_len)
# ncols = int(ncols)
# nrows = int(nrows)
# g, eq_time = load_tsun( sf_list, gauges, eq_path)
# # g_trim, eq_time_trim = trim(g, eq_time)
# # plot_gauges(gauges, waves, time, g, eq_time)
# for i, v in enumerate(loop):
#    fig =  create_group_plot(ar_len, i, v, gauges, waves, time, g, eq_time, nrows, ncols)
# plt.rcParams['font.size'] = 18
# fig.text(0.5, 0.03, 'Time (minutes)', ha='center', va='center')
# fig.text(0.08, 0.5, 'Wave Amplitude (m)', ha='center', va='center', rotation=90)
#    # plt.savefig('Figure3_waves.png')
#
# plt.savefig('Figure3_waves.png')
# plt.savefig('Figure3_waves.ps')