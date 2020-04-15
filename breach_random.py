import numpy as np
from random import uniform
from shutil import copyfile

def randomize_breach(lat, lon, depth, breach_flag):
    # if (lat >= 27.91854 and lat <= 27.93569):
    y = lat
    x = lon
    x1 = lon + 0.02
    x2 = lon - 0.02
    file_name = '{}_{}.txt'.format(x, abs(y))
    print(file_name)
    with open(file_name, 'w') as f:
        f.write('{}\n{}\n{}\n{}\n{}\n'.format(breach_flag, x1, x2, y, depth))
    f.close()

#
# frand = [uniform(-85.0, -83.0) for i in (0, 1)]
# print(frand)
#
# randomize_breach(-85.0, 27.92, 1, 1)
def replace_line(file_name, line_num, text):
    """
    Replace line in respective file. Please note that the line
    numbering starts at zero.
    """
    lines = open(file_name, 'r').readlines()
    out = open(file_name, 'w')

    lines[line_num] = text
    out.writelines(lines)
    out.close()
    # lines.close()

line_nums = [42, 43, 44, 45, 46, 47]
file = 'b4step2_test.f90'
flag = 1
lat0 = 27.80
lat1 = 28.2
lon0 = [-91.0, -90.0, -92.0]
lon1 = [-89.0, -88.0, -90.0]
mu = [-90.0, -89.0, -91.0]



file_prefix = 'b4step2'
file_type = '.f90'
file_seq = [0, 1, 2]
new_file = []
for f in file_seq:
    new_file.append(file_prefix + '_{}'.format(f) + file_type)

    text = ['breach_trigger = {}\n'.format(flag), 'lat0 = {}\n'.format(lat0), 'lat1 = {}\n'.format(lat1),
            'lon0 = {}\n'.format(lon0[f]), 'lon1 = {}\n'.format(lon1[f]), 'mu = {}\n'.format(mu[f])]
    for f in new_file:
        for idx, l in enumerate(line_nums):
            replace_line(file, l, text[idx])
    copyfile(file, f)

# replace_line(file, line_nums, text)