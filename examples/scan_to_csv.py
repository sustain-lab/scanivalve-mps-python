"""
scan_to_csv.py - Scan and save to a CSV file.
"""

RUN_NAME = "run"      # the output file will be called <RUN_NAME>_<TIMESTAMP>.csv
FRAMES_PER_SCAN = 100 # how many frames to take
RATE = 10             # number of samples / channel / second (Hz)
UNITS = "PA"          # units; see the manual for what's available

print('Welcome to MPS4264')
print()
print('Run name: ' + RUN_NAME)
print('Frames to take: ' + str(FRAMES_PER_SCAN))
print('Frame rate: ' + str(RATE) + ' Hz')
print()

# you shouldn't need to edit below this line

from scanivalve_mps.mps import MPS
from datetime import datetime

MPS_HOST = "191.30.90.1"

mps = MPS(MPS_HOST)

if not mps.status() == 'ready':
    raise RuntimeError('MPS is not ready; try again later.')

print('Starting zero calibration. This will take 15 seconds or so...')
mps.calibrate_zero()
print('Calibration done.')

now = datetime.now()
print('Setting time to ', now)
res = mps.set_time(now)

mps.set_format('csv')
mps.set_frames_per_scan(FRAMES_PER_SCAN)
mps.set_rate(RATE)
mps.set_scan_units('PA')

output_file = 'run_' + now.strftime('%Y-%m-%d_%H_%M_%S') + '.csv'
mps.scan_to_csv(output_file)

mps.disconnect()

print('Data written to ' + output_file)
input()