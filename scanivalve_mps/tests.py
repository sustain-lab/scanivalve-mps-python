from datetime import datetime
import time
from scanivalve_mps.mps import MPS
from scanivalve_mps.tcp import tcp_decode, tcp_encode

HOST = '191.30.90.1'
PORT = 23

def test_tcp_decode():
    assert tcp_decode(b'hello\r\n') == ['hello']

def test_tcp_encode():
    assert tcp_encode('hello') == b'hello\r\n'

def test_mps_init():
    mps = MPS(HOST, PORT)
    assert type(mps) is MPS
    mps.disconnect()

def test_mps_bootloader_version():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    assert 'BOOTLOADER VERSION' in mps.bootloader_version()
    mps.disconnect()

def test_mps_get_scan_start_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    mps_time = mps.get_scan_start_time()
    assert type(mps_time) is datetime

def test_mps_get_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    mps_time = mps.get_time()
    assert type(mps_time) is datetime

def test_mps_set_time():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    t = datetime.now()
    mps_time = mps.set_time(t)
    assert type(mps_time) is datetime

def test_mps_status():
    time.sleep(0.2) # sleep to make sure the socket is closed from previous test
    mps = MPS(HOST, PORT)
    status = mps.status()
    assert type(status) is str
    mps.disconnect()

def test_mps_version():
    time.sleep(0.2)
    mps = MPS(HOST, PORT)
    version = mps.version()
    assert 'MPS Scanivalve' in version
    mps.disconnect()

