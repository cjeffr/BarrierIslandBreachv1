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

def plot_gauges(gauges, wave, time_interval, g, eq_time,g_name, sim):

    print('len gauges = ', len(wave))
    fig =  plt.figure()

    plt.subplots_adjust(hspace=0.000)
    plt.gca().yaxis.set_minor_formatter(ticker.NullFormatter())


    loop = np.arange(0,9) #[18, 19, 1, 4, 5, 6, 7, 8, 9, ]

    t_min = eq_time[0] / 60 / 60 / 24
    t_max = eq_time[-1] / 60 / 60 / 24
    g_range = t_max - t_min
    d_range = eq_time[-1] - eq_time[0]
    r = g_range / d_range
    xa = [x * r for x in eq_time]

    plt.plot(eq_time,g, 'k--', label='No Breach')
    rainbow = plt.get_cmap('rainbow')
    colors = iter(rainbow(np.linspace(0, 1, len(gauge_data))))

    s = 1
    for gauge in wave:
        # tick_min = gauge[1][0] / 60 / 60 / 24
        # tick_max = gauge[1][-1] / 60 / 60 / 24
        # graph_range = tick_max - tick_min
        # data_range = gauge[1][-1] - gauge[1][0]
        # ratio = graph_range / data_range
        # xax = [x * ratio for x in gauge[1]]
        plt.plot(gauge[1], gauge[2], color=next(colors), label='Simulation {}'.format(s))
        s+=1

    plt.title('Gauge {}'.format(wave[0][0]))
    plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)

    plt.xlabel("Days from landfall", fontsize=16)  # declare the x axis label
    plt.ylabel("Wave Amplitude (m)", fontsize=16)
    # plt.axhline(y=0.00, xmin=0, xmax=14400, c='black', linewidth=.5, zorder=0)  # draw a zero line
    # plt.xticks([],
    #            [x for x in range(tick_min_days, tick_max_days)])
    plt.legend(loc='upper left')
    plt.savefig('GaugeNumber {}.png'.format(g_name))
    plt.show()
    # plt.savefig('{}.png'.format(wave[0][0]))


sgf_path = '/mnt/c/storm/v5_done/'
sims = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
gauges = np.arange(0, 40)
for g in gauges:

    gauge_no = []
    gauge_data = []
    time_data = []
    compare = os.path.join('/mnt/c/storm/v5_done/no_breach/_output', 'gauge{:05d}.txt'.format(g))
    w = np.genfromtxt(compare, usecols=5, dtype='float')
    time = np.genfromtxt(compare, usecols=1, dtype='float')
    for s in sims:
        gauge_file = os.path.join(sgf_path, 's{}/_output'.format(s), 'gauge{:05d}.txt'.format(g))

        gauge_no.append(s)
        times = np.genfromtxt(gauge_file, usecols=1, dtype='float')
        data = np.genfromtxt(gauge_file, usecols=5,  dtype='float')
        gauge_data.append((g, times, data))
        time_data.append(times)
    print(len(gauge_data))
    plot_gauges(gauge_no, gauge_data, time_data, w, time,g, s)
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