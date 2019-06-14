from scanivalve_mps.mps import MPS
from datetime import datetime
import os

host = os.environ['MPS_HOST']

mps = MPS(host)
print(mps.bootloader_version())
print(mps.status())
print(mps.get_time())
print(mps.get_scan_start_time())
print(mps.set_time(datetime.now()))

print('Zero calibration..')
mps.calibrate_zero()

mps.set_format('csv')
mps.set_frames_per_scan(100)
mps.set_rate(10)
#print(mps.scan())
mps.set_scan_units('PA')
mps.scan_to_csv('test.csv')
mps.disconnect()
