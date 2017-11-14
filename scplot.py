# This script will plot whatever search coil data is in the current folder.
# TODO: Put datetimes on the x axis
#       Label the plots
#       Adjust the timeseries so they line up with the specgrams
#       Modularize, yada yada

import os
import gzip
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

##############################################################################
# IMPORT

zip_list = [s for s in os.listdir() if s.endswith('.dat.gz')]
hex = b''
for file in zip_list:
    with gzip.open(file, mode='rb') as bitstream:
        hex = hex + bitstream.read()

##############################################################################
# PROCESS

# merge all binary values into a single stream
# NOTE: This also fixes the stripped leading zeros from read
binstr = ''.join(['{:08b}'.format(x) for x in hex])
# separate the stream into 12bit ADC values
binstr = [binstr[i:i + 12] for i in range(0, len(binstr), 12)]
# convert the binary values to integers
intstr = [int(x, 2) for x in binstr]
intstr = [x - 4096 if x > 2047 else x for x in intstr]
# group the X/Y by sample
all_samples = [intstr[i:i + 2] for i in range(0, len(intstr), 2)]
# cleanup
del binstr
del intstr

# numpyfy the x values
x_samples = np.array([x[0] for x in all_samples])
# scale them to our system (bit conversion / ADC Gain)
x_samples = x_samples * (.0049 / 4.43)

# numpyfy the y values
y_samples = np.array([x[1] for x in all_samples])
# scale them to our system (bit conversion / ADC Gain)
y_samples = y_samples * (.0049 / 4.43)

##############################################################################
# PLOTS

f, axs = plt.subplots(4)

axs[0].plot(x_samples)
axs[0].axis([0, 864000, -0.25, 0.25])

axs[1].specgram(x_samples, NFFT=1024, noverlap=256 * 3, Fs=10,
                cmap='terrain', scale='dB')
for im in axs[1].get_images():
    im.set_clim(-60, 0)
divider = make_axes_locatable(axs[1])
cax = divider.append_axes("right", "2%", pad="1%")
plt.colorbar(im, cax=cax)

plt.tight_layout()

axs[2].plot(y_samples)
axs[2].axis([0, 864000, -0.25, 0.25])

axs[3].specgram(y_samples, NFFT=1024, noverlap=256 * 3, Fs=10,
                cmap='terrain', detrend='linear', scale='dB')
for im in axs[3].get_images():
    im.set_clim(-60, 0)
divider = make_axes_locatable(axs[3])
cax = divider.append_axes("right", "2%", pad="1%")
plt.colorbar(im, cax=cax)

plt.show()

exit()
