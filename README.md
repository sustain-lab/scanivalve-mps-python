# scanivalve-mps-python

A Python interface to Scanivalve MPS4264.

## Getting started

### Get the code and set up the environment

```
git clone https://github.com/sustain-lab/scanivalve-mps-python
scanivalve-mps-python
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### Run tests

The instrument must be connected and powered to run the tests succesfully.

```
pytest -v scanivalve_mps/tests.py
```

## Supported functions

* [x] `MPS.bootloader_version()`
* [x] `MPS.status()`
* [x] `MPS.get_time()`
* [ ] `MPS.set_time()`
