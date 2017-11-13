# This script will plot whatever decompressed search coil data is in the current folder.
# TODO: Import the bitstream into a numpy array sooner
#       Other speed related tasks
#       Read encrypted files
#       Modularize, yada yada

import os
import numpy as np
import matplotlib.pyplot as plt

filelist = [x if '.' not in x else '' for x in os.listdir() if '.' not in x]
hex = b''
for file in filelist:
    with open(file, mode='rb') as bitstream:
        hex = hex + bitstream.read()
# merge all binary values into a single stream
# NOTE: This also fixes the leading zeros
second = ''.join(['{:08b}'.format(x) for x in hex])
# separate the stream into 12bit ADC values
binsec = [second[i:i + 12] for i in range(0, len(second), 12)]
# convert the binary values to integers
sec1 = [int(x, 2) for x in binsec]
sec1 = [x - 4096 if x > 2047 else x for x in sec1]
# group the X/Y by sample
xy = [sec1[i:i + 2] for i in range(0, len(sec1), 2)]
xs = [x[0] for x in xy]
xs = np.array(xs)
xs = xs * (.0049 / 4.43)

plt.specgram(xs, NFFT=1024, noverlap=256 * 3, Fs=10,
             cmap='terrain', scale='dB')
plt.ylim(ymax=1)
plt.clim(0, -60)
plt.colorbar()
plt.show()

ys = [x[1] for x in xy]
ys = np.array(ys)
ys = ys * (.0049 / 4.43)
plt.subplot(212)
plt.specgram(ys, NFFT=1024, noverlap=256 * 3, Fs=10,
             cmap='winter', detrend='linear', scale='dB')
plt.colorbar()
plt.show()

exit()
