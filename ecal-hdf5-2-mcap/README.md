# ecal-hdf5-2-mcap

This tool is a helper script to convert measurements from eCAL HDF5 measurement format to the Foxglove mcap format.
Converted files can be imported directly into Foxglove Studio.

## Setup
For installation, you will need a recent Python version (>= 3.8).
We recommend to setup the Bridge in an isolated Python environment.

Please download the Python wheel matching to your eCAL installation and OS from the [Github Release Page](https://github.com/eclipse-ecal/ecal/releases).
As eCAL is not yet available as a PyPi package, it cannot be installed automatically via pip.
You will need an eCAL version `>=3.11.0` for the tool to work.

Then install all requirements plus the eCAL wheel:
```
pip install -r requirements.txt
pip install /path/to/ecal-wheel.whl
```

## Usage

After installing all requirements, the bridge can be launched by running

```
python ./ecal-hdf5-2-mcap.py --help
usage: ecal-hdf5-2-mcap.py [-h] [-o OUTPUT] input

Conversion Script eCAL HDF5 to MCap

positional arguments:
  input                 Path to eCAL measurement as folder or file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to converted measurement
```
