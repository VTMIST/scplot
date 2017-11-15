# This script will plot whatever search coil data is in the current folder.
# TODO: Modularize, yada yada

import os
import gzip
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

##############################################################################
# IMPORT

scpath = './'
sc_zip_list = [s for s in os.listdir(scpath) if s.endswith('.dat.gz')]
hex = b''
datetimes = []
sample_rate = dt.timedelta(microseconds=100000)
for file in sc_zip_list:
    file_start = dt.datetime.strptime(file[3:22], '%Y_%m_%d_%H_%M_%S')
    with gzip.open(scpath + file, mode='rb') as bitstream:
        in_bits = bitstream.read()
        hex = hex + in_bits
        in_dates = [file_start + sample_rate *
                    x for x in range(0, len(in_bits) // 3)]
        datetimes = datetimes + in_dates

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

hours = mdates.HourLocator(interval=2)
hourFmt = mdates.DateFormatter('%H:00')

fig = plt.figure()
ax0 = fig.add_subplot(411, label="Xspec")
ax1 = fig.add_subplot(412, label="Xseri")
ax2 = fig.add_subplot(413, label="Yspec")
ax3 = fig.add_subplot(414, label="Yseri")
ax01 = fig.add_subplot(411, label="Xspec2", frame_on=False)
ax21 = fig.add_subplot(413, label="Yspec2", frame_on=False)

s, f, t, im = ax0.specgram(x_samples, NFFT=1024, noverlap=256 * 3, Fs=10,
                           cmap='terrain', scale='dB')
im.set_clim(-60, 0)
ax0.set_xticklabels([])
# divider = make_axes_locatable(axs[1])
# cax = divider.append_axes("right", "2%", pad="1%")
# plt.colorbar(im, cax=cax)

ax01.plot(datetimes, x_samples, 'None')
ax01.set_yticklabels([])
ax01.xaxis.set_major_locator(hours)
ax01.xaxis.set_major_formatter(hourFmt)

ax1.plot(datetimes, x_samples)
ax1.margins(0, 0)
ax1.xaxis.set_major_locator(hours)
ax1.xaxis.set_major_formatter(hourFmt)

s, f, t, im = ax2.specgram(y_samples, NFFT=1024, noverlap=256 * 3, Fs=10,
                           cmap='terrain', scale='dB')
im.set_clim(-60, 0)
ax2.set_xticklabels([])
# divider = make_axes_locatable(axs[3])
# cax = divider.append_axes("right", "2%", pad="1%")
# plt.colorbar(im, cax=cax)

ax21.plot(datetimes, x_samples, 'None')
ax21.set_yticklabels([])
ax21.xaxis.set_major_locator(hours)
ax21.xaxis.set_major_formatter(hourFmt)

ax3.plot(datetimes, y_samples)
ax3.margins(0, 0)
ax3.xaxis.set_major_locator(hours)
ax3.xaxis.set_major_formatter(hourFmt)

plt.show()

exit()
