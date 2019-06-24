from setuptools import setup

setup(
    name='scanivalve-mps-python',
    version='0.1.0',
    description='Python interface to Scanivalve MPS4264',
    author='Milan Curcic',
    author_email='mcurcic@miami.edu',
    url='https://github.com/sustain-lab/scanivalve-mps-python',
    packages=['scanivalve_mps'],
    install_requires=['pytest'],
    test_suite='scanivalve_mps.tests',
    license='MIT'
)
