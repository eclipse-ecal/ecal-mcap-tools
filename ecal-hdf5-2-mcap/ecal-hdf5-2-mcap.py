import argparse
import os
import pathlib
import sys
import time

import semver
from ecal.core.core import getversion
#check for proper eCAL version!
version = getversion()
if not semver.match(version[1:], ">=5.11.0"):
  sys.exit("Please check your eCAL version. It needs to be >= 5.11.0, but your version is {}.".format(version[1:]))

from ecal.measurement.measurement import Measurement, BinaryChannel
from mcap.writer import Writer, CompressionType

from argparse import ArgumentParser
import sys

def main(args):
  # Create a measurement (pass either a .hdf5 file or a measurement folder)
  measurement = Measurement(args.input, channel_access_mode = Measurement.ChannelAccessMode.BINARY)
  stream = open(args.output, "wb")
  writer = Writer(stream)
 
  # Retrieve the channels in the measurement by calling measurement.channel_names
  writer.start(profile="x-custom", library="ecal-hdf5-2-mcap")

  # You can iterate over all channels in a measurement
  for channel in measurement.channel_names:
    binary_channel = measurement[channel]

    if (binary_channel.type_encoding != "proto"):
      continue

    print("Converting channel {}.".format(channel))

    schema_id = writer.register_schema(
      name=binary_channel.type_name,
      encoding="protobuf", # take real encoding from info
      data=binary_channel.type_descriptor
    )

    channel_id = writer.register_channel(
      schema_id=schema_id,
      topic=binary_channel.topic_name,
      message_encoding="protobuf"
    )

    for entry in binary_channel:
      writer.add_message(
        channel_id=channel_id,
        log_time=entry.rcv_timestamp*1000,
        data=entry.msg,
        publish_time=entry.snd_timestamp*1000,
      )

  writer.finish()

# Valid eCAL measurements are either a folder path or a path to a .hdf5 file.
def ecal_hdf5_meas(astring):
    path = pathlib.Path(astring)
    exists =  path.exists()
    folder_or_hdf5 = path.is_dir() or path.suffix == ".hdf5"
    if not (exists and folder_or_hdf5):
        raise argparse.ArgumentTypeError("{} is not a valid eCAL measurement. Please make sure that the path exists and that it is either a folder or a '.hdf5' file.".format(astring))  # or TypeError, or `argparse.ArgumentTypeError
    return astring


def parse_arguments():
  parser = ArgumentParser(description="Conversion Script eCAL HDF5 to MCap")
  parser.add_argument("input", type=ecal_hdf5_meas, help="Path to eCAL measurement as folder or file")
  parser.add_argument("-o", "--output", type=str, help="Path to converted measurement", required=False)
  
  args = parser.parse_args()    
  
  # if no output is given, use input.mcap as output file
  if not args.output:
    input_path = pathlib.Path(args.input)
    if input_path.is_dir():
      # just append .mcap to make it a filename. otherwise .with_suffix will remove stuff in folder name after a '.'
      args.output = str(input_path) + ".mcap"
    else:
      args.output = str(input_path.with_suffix('.mcap'))
  
  return args


if __name__ == "__main__":
  args = parse_arguments()
  main(args)  