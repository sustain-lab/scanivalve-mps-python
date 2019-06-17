# scanivalve-mps-python

A Python interface to [Scanivalve MPS4264](http://scanivalve.com/products/pressure-measurement/miniature-ethernet-pressure-scanners/mps4264/).

## Getting started

### Get the code and dependencies

```
git clone https://github.com/sustain-lab/scanivalve-mps-python
scanivalve-mps-python
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### Set the environment

`MPS_HOST` environment variables must be set 
to the IP address of the sensor (see label on the bottom side).
For example:

```
export MPS_HOST=191.30.90.1
```

### Run tests

The instrument must be connected and powered to run the tests succesfully.

```
pytest -v scanivalve_mps/tests.py
```

### Example use

```python
from datetime import datetime
import os
from scanivalve_mps.mps import MPS

host = os.environ['MPS_HOST']

mps = MPS(host)
mps.set_time(datetime.utcnow())

print('Zero calibration...')
mps.calibrate_zero()

# set up the scan parameters
mps.set_format('csv')
mps.set_scan_units('PA')
mps.set_frames_per_scan(100)
mps.set_rate(10)
mps.scan_to_csv('test_run.csv')

mps.disconnect()
```

## Supported functions

* [x] `MPS.bootloader_version()`
* [x] `MPS.calibrate_zero()`
* [x] `MPS.get_scan_start_time()`
* [x] `MPS.get_time()`
* [x] `MPS.scan()`
* [x] `MPS.scan_to_csv(filename)`
* [x] `MPS.set_format(format_code)`
* [x] `MPS.set_frames_per_scan(fps)`
* [x] `MPS.set_rate(rate)`
* [x] `MPS.set_scan_units(units)`
* [x] `MPS.set_time(time)`
* [x] `MPS.status()`
* [x] `MPS.stop()`
* [x] `MPS.stream(frames)`
* [x] `MPS.version()`
