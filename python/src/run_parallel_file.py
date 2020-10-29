import os

with open('command.test', 'w') as f:
    for i in range(10):
        f.write('cd sim{}_1/;make .plots\n'.format(i))
f.close()
