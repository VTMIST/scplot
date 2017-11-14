# scplot
Search Coil Magnetometer Plotting Script

This is the MIST team's prospective new method of plotting its search coil magnetometer data.
The current usage is to run this python script in the same folder as whatever raw SC data you want to plot.
NOTE: This is written for Python 3.

Major items that need to be addressed:
  * Timestamps on the X axis of each spectrogram
  * Additionally plot the timeseries data
  * Speed up processing by converting to numpy arrays sooner
  * Better options for input handling
  * Format the code as a proper importable module (declare functions, etc)

For now, it works.
