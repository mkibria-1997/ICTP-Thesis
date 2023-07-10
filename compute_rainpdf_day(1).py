#!/usr/bin/env python3

import glob
import xarray as xr
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt

rain_minimum = 1.0
rain_maximum = 250.0
rain_step = 1.0
spd = 86400.0
sph = 3600.0

nrainbin = int((rain_maximum-rain_minimum)/rain_step) + 1

rain_pdf = np.linspace(rain_minimum,rain_maximum, num=nrainbin, endpoint=True)
rain_bin = np.zeros((nrainbin-1))

for ncfile in glob.glob('output/*STS.??????????.nc'):
    print(ncfile)
    pr = xr.load_dataset(ncfile)
    size = pr.pr.shape
    for time in range(size[0]):
        data =  pr.pr[time,Ellipsis] * spd
        nzd = data.values[tuple(np.where(data >= rain_minimum))]
        hist = np.histogram(nzd,
                            bins = nrainbin-1,
                            range = (rain_minimum, rain_maximum))
        rain_bin = rain_bin + hist[0]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.plot(rain_bin, 'ro')
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlabel('Precimitation [mm/d]')
plt.ylabel('Event Number [#]')
plt.title('Precipitation daily PDF')
plt.show( )
