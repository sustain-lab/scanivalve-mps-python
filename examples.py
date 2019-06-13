from scanivalve_mps.mps import MPS
from datetime import datetime

HOST = '191.30.90.1'
PORT = 23

mps = MPS(HOST, PORT)
print(mps.bootloader_version())
print(mps.status())
print(mps.get_time())
print(mps.get_scan_start_time())
print(mps.set_time(datetime.now()))
print(mps.set_format('csv'))
print(mps.scan())
mps.disconnect()
