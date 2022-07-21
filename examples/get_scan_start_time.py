from datetime import datetime
from scanivalve_mps.mps import MPS

HOST = '10.126.0.150'
mps = MPS(HOST)

t = mps.get_scan_start_time()

print(t)

mps.disconnect()

input('Done. Press Enter to exit..')
