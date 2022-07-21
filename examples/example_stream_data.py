from scanivalve_mps.mps import MPS
from datetime import datetime
import os

host = os.environ['MPS_HOST']

mps = MPS(host)

if not mps.status() == 'ready':
    raise RuntimeError('MPS is not ready; try again later.')

now = datetime.now()
print('Setting time to ', now)
res = mps.set_time(now)

print('Starting zero calibration. This will take 15 seconds or so...')
mps.calibrate_zero()
print('Calibration done.')

mps.set_format('csv')
mps.set_frames_per_scan(100)
mps.set_rate(10)
mps.set_scan_units('PA')
mps.stream()
mps.disconnect()
