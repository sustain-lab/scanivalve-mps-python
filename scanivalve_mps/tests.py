from datetime import datetime
import os
import time
from scanivalve_mps.mps import MPS
from scanivalve_mps.tcp import tcp_decode, tcp_encode

HOST = os.environ['MPS_HOST']

def test_tcp_decode():
    assert tcp_decode(b'hello\r\n') == ['hello']

def test_tcp_encode():
    assert tcp_encode('hello') == b'hello\r\n'

def test_mps_init():
    mps = MPS(HOST)
    assert type(mps) is MPS
    mps.disconnect()

def test_mps_bootloader_version():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    assert 'BOOTLOADER VERSION' in mps.bootloader_version()
    mps.disconnect()

def test_mps_get_scan_start_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    mps_time = mps.get_scan_start_time()
    assert type(mps_time) is datetime

def test_mps_get_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    mps_time = mps.get_time()
    assert type(mps_time) is datetime

def test_mps_scan():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    mps.set_frames_per_scan(1)
    data = mps.scan()
    assert type(data) is list
    assert len(data) == 2

def test_mps_scan_to_csv():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    mps.set_frames_per_scan(1)
    test_file = 'test_scan.csv'
    mps.scan_to_csv(test_file)
    assert os.path.exists(test_file)
    os.remove(test_file)

def test_mps_set_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    t = datetime.now()
    mps_time = mps.set_time(t)
    assert type(mps_time) is datetime

def test_mps_status():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST)
    status = mps.status()
    assert type(status) is str
    mps.disconnect()

def test_mps_version():
    time.sleep(0.2)
    mps = MPS(HOST)
    version = mps.version()
    assert 'MPS Scanivalve' in version
    mps.disconnect()

def test_mps_calibrate_zero():
    time.sleep(0.2)
    mps = MPS(HOST)
    mps.calibrate_zero()
    assert True
    mps.disconnect()
