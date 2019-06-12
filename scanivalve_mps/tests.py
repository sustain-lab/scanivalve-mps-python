from datetime import datetime
import time
from scanivalve_mps.mps import MPS

HOST = '191.30.90.1'
PORT = 23

def test_mps_init():
    mps = MPS(HOST, PORT)
    assert type(mps) is MPS
    mps.disconnect()

def test_mps_bootloader_version():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    assert 'BOOTLOADER VERSION' in mps.bootloader_version()
    mps.disconnect()

def test_mps_get_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    mps_time = mps.get_time()
    assert type(mps_time) is datetime

def test_mps_status():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    status = mps.status()
    assert type(status) is str
    mps.disconnect()
