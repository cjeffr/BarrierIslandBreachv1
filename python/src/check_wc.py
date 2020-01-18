"""
A file to check the lengths of tsunami green's functions to ensure they're all the same length
"""

import os
import subprocess
#sf = [9,10,11,12,'8-12']
#slip = [1, 5, 10, 15, 20]
# for fault in sf:
#     for s in slip:
path='/mnt/c/fortranprograms/gauges_done/gauges1' # .format(fault, s) #"/Users/jeffriesc/clawpack-5.4.1/geoclaw/examples/tsunami/SF_{}_{}m/_output".format(fault, s)

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
print(path)
for f in files:
    if f.startswith('gauge'):
        lines = open(os.path.join(path, f)).readlines()

        print( "file " + f + " has %d lines" % len(lines))