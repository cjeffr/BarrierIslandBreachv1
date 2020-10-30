import os
import subprocess
import numpy as np
import shutil

def random_width(v):
    """
    randomize the variables for breaching, must include the outer limits of where breach should occur
    :param lat_range:
    :param lon_range:
    :return:
    """
    lat = b[0]
    lon = b[1]
    lat0 = lat - .025
    lat1 = lat + .025
    width = np.random.uniform(30.0, 300.0)
    m_res = 10  # 10 (m) resolution
    sec_per_degree = 3600
    breach = (width / 30) / sec_per_degree  # 25m minimum breach width (in degrees)
    lon0 = lon - breach
    lon1 = lon + breach
    return lat0, lat1, lon0, lon1, width

def create_breach_data(lat0, lat1, mu, lon0, lon1, sigma, time_factor, start_time, end_time):
    header = 'breach_trigger, lat0, lat1, lon0, lon1, mu, sigma, time_factor, start_time, end_time\n'
    data = f'1\n{lat0}\n{lat1}\n{lon0}\n{lon1}\n{mu}\n{sigma}\n{time_factor}\n{start_time}\n{end_time}'

    with open('breach.data', 'w') as f:
        f.write(header)
        f.write(data)
    f.close()

    shutil.copyfile('breach.data', os.path.join(dir_name, 'breach.data'))

def create_dir(folder):
    """
    create directory for each folder name
    :param folder:
    :param file_content:
    :param filename:
    :return:
    """
    files = ['Makefile', 'b4step2.f90', 'setprob.f90', 'breach_module.f90', 'setrun.py', 'setplot.py']
    if not os.path.exists(folder):
        os.mkdir(folder)

    for f in files:
        copy_loc = os.path.join(folder, f)
        orig_loc = os.path.join('geoclaw_files', f)
        shutil.copyfile(orig_loc, copy_loc)




# Declare possible breach locations
breach_location = [(40.813051, -72.577037), (40.816357, -72.563482), (40.817740, -72.559827),
                   (40.822937, -72.544451), (40.823036, -72.542743), (40.823440, -72.540075),
                   (40.832282, -72.571093)]
storm = 'sandy'
time_factor = 0.2
start_time = -25200
end_time = -21600
sigma = 1.0
# Randomize breach location
for b in breach_location:
    lat0, lat1, lon0, lon1, width = random_width(b)
    mu = b[1]
    dir_name = f'{storm}_{b[0]}_{b[1]}_{width}'
    create_dir(dir_name)
    create_breach_data(lat0, lat1, mu, lon0, lon1, sigma, time_factor, start_time, end_time)
    os.chdir(dir_name)
    subprocess.run(['make', 'new'])
    subprocess.run(['make', '.plots'])
    os.chdir('../setup')






# Create folder based on storm/lat/lon/width/depth?

# copy files to new folder

# chdir to folder and run geoclaw

# go back to first folder repeat
