from shutil import copyfile
import os
import random

"""
This collection of scripts enables random breach variables to be automatically generated, written to text file and 
copies (along with other files) to a folder numbered sequentially that can then be used for simulations
"""


def randomize_breach(lat, lon, depth, breach_flag):
    """

    :param lat: latitude of breach
    :param lon: longitude of breach
    :param depth:
    :param breach_flag: turn breach on or not
    :return: just writes a file
    """

    y = lat
    x = lon
    x1 = lon + 0.02
    x2 = lon - 0.02
    file_name = '{}_{}.txt'.format(x, abs(y))
    print(file_name)
    with open(file_name, 'w') as f:
        f.write('{}\n{}\n{}\n{}\n{}\n'.format(breach_flag, x1, x2, y, depth))
    f.close()


def replace_line(file_name, line_num, text):
    """
    Replace line in respective file. Please note that the line
    numbering starts at zero.
    :param file_name: name of file to be modified
    :param line_num: which line numbers to change
    :param text: text to change per line number
    :return: just writes to file
    """
    lines = open(file_name, 'r').readlines()
    out = open(file_name, 'w')
    lines[line_num] = text
    print(text)
    out.writelines(lines)
    out.close()


def calc_time_factor(start_breach, end_breach):
    """
    calculates the fraction of island height to be reduced during simulation
    :param start_breach: start time (island should be inundated here)
    :param end_breach: end time
    :return: return the timing ratio
    """
    total_time = abs(end_breach - start_breach)
    num_time_steps = total_time / 7.5  # current run timesteps every 7.5 seconds or so
    tf = 1 / num_time_steps  # calculate how many steps it takes to reach 100% breach
    return tf


def make_folder_list(number):
    """
    Generates a list of folder names to be created
    :param number: total number of folders to generate
    :return: returns the list of all folders
    """
    folder_list = []
    for i in range(number):
        name = f'sim_{i:04}'
        folder_list.append(name)
    return folder_list


def set_variables(lat_range, lon_range):
    """
    randomize the variables for breaching, must include the outer limits of where breach should occur
    :param lat_range:
    :param lon_range:
    :return:
    """
    lat0 = lat_range[0]
    lat1 = lat_range[1]
    mu = random.uniform(lon_range[0], lon_range[1])
    m_res = 10  # 10 (m) resolution
    sec_per_degree = 3600
    min_breach = m_res * 28 / sec_per_degree  # 25m minimum breach width (in degrees)
    max_breach = m_res * 600 / sec_per_degree  # 600m max breach width (in degrees)
    random_breach = random.uniform(min_breach, max_breach)
    lon0 = mu - random_breach
    lon1 = mu + random_breach
    return lat0, lat1, lon0, lon1, mu


def create_dir(folder, file_content, filename):
    """
    create directory for each folder name
    :param folder:
    :param file_content:
    :param filename:
    :return:
    """
    os.mkdir(folder)
    copyfile(filename, folder)

# This section runs the above functions
lat = [29.51, 29.53]
lon = [-94.0, -96.0]
lat0, lat1, lon0, lon1, mu = set_variables(lat_range=lat, lon_range=lon)
file_prefix = 'breach'
file_type = '.data'
files = ['Makefile', 'b4step2.f90', 'setprob.f90', 'breach_module.f90', 'setrun.py', 'setplot.py']

folder_list = make_folder_list(2)
file_list = []
start_time = -58400
end_time = -54000
time_factor = calc_time_factor(start_time, end_time)
for folder in folder_list:
    fl = int(folder.split('_')[1])
    if fl == 0:
        lat0, lat1, lon0, lon1, mu = set_variables(lat_range=lat, lon_range=lon)
        breach_trigger = 0
    else:
        breach_trigger = 1
    new_file = folder + '/' + file_prefix + file_type

    if not os.path.exists(folder):
        os.mkdir(folder)
    for cf in files:
        copy_loc = folder + '/' +  cf
        copyfile(cf, copy_loc)

    header = 'breach_trigger, lat0, lat1, lon0, lon1, mu, sigma, time_factor, start_time, end_time\n'
    data = f'{breach_trigger}\n{lat0}\n{lat1}\n{lon0}\n{lon1}\n{mu}\n{time_factor}\n{start_time}\n{end_time}'

    with open(new_file, 'w') as f:
        f.write(header)
        f.write(data)
    f.close()

