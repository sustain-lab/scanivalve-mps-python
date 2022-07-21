from datetime import datetime
from scanivalve_mps.mps import MPS

HOST = '10.126.0.150'
mps = MPS(HOST)

t1 = datetime.utcnow()
print('sync_mps_clock started at', t1)
while True:
    t2 = datetime.utcnow()
    if t2.microsecond < t1.microsecond:
        mps.set_time(t2)
        mps_time = mps.get_time()
        break
    t1 = t2

print('sync_mps_clock synced at', t2)
print('sync_mps_clock MPS time is', mps_time)

print('Disconnecting from MPS..')
mps.disconnect()

input('Done. Press Enter to exit..')
