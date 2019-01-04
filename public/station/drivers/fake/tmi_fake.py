#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
import argparse
from pubsub import pub
from app.const import TMI_PUB

TMI_VERSION = "0.0.1"

NUM_CHANNELS = 1  # set this to simulate multiple channels


class TMIHWDriver(object):
    """
    TMIHWDriver is a class that installs a HW driver into the shared state.
    This is not the HW driver itself, just an installer.

    When a script is loaded, there is a config section that lists all the TMIHWDriver
    to call, for example,

      "config": {
        # channel_hw_driver: list of code to initialize the test environment, must be specified
        "channel_hw_driver": ["public.scripts.TMIDemoRecordV1.prod_v0.drivers.tmi_fake"]
      },

    channel_hw_driver is a list, so multiple TMIHWDriver can be called.

    This is a fake HW driver to simulate and show what a TMIHWDriver is required to do.
    """

    def __init__(self, shared_state):
        self.logger = logging.getLogger("TMI.{}".format(__class__.__name__))
        self.logger.info("Start")
        self.shared_state = shared_state

    def discover_channels(self):
        """ determine the number of channels, and popultae hw drivers into shared state

        shared_state: a list,
            self.shared_state.add_drivers(DRV_TYPE, [ {}, {}, ... ], shared=True/False)

        [ {'id': i,               # id of the channel (see Note 1)
           "version": <VERSION>,  # version of the driver
           "close": False},       # register a callback on closing the channel
           "<foo>": <bar>,        # something that makes your HW work...
        ]

        Note:
        1) The hw driver objects are expected to have an 'id' field, the lowest
        id is assigned to channel 0, the next highest to channel 1, etc

        :return: >0 number of channels,
                  0 does not indicate num channels, like a shared hardware driver
                 <0 error
        """
        drivers = []
        for i in range(NUM_CHANNELS):

            # drivers must have an 'id' field, and then whatever...
            # close field is a method called when channel is torn down
            drivers.append({'id': i, "version": TMI_VERSION, "close": False})

            dd = {"notice": "TMIHWDriver: Found channel {}".format(i),
                  "from": "{}.{}".format(__class__.__name__, "discover_channels")}
            pub.sendMessage(TMI_PUB.TMI_FRAME_SYSTEM_NOTICE, item_dict=dd)

        self.shared_state.add_drivers("TMIFake", drivers)
        self._num_chan = NUM_CHANNELS
        self.logger.info("{} channels found".format(self._num_chan))
        return self._num_chan

    def num_channels(self):
        return self._num_chan

    def init_play_pub(self):
        """ Function to instantiate a class/thread to trigger PLAY of script
        - this is called right after discover_channels
        """
        self.logger.info("TMIFake does not support 'play' messaging")

    def close(self):
        self.logger.info("closed")


def parse_args():
    epilog = """
    Usage examples:
    """
    parser = argparse.ArgumentParser(description='tmi_fake',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)

    parser.add_argument("-v", '--verbose', dest='verbose', default=0, action='count', help='Increase verbosity')
    parser.add_argument("--version", dest="show_version", action='store_true', help='Show version and exit')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    logger = logging.getLogger()
    args = parse_args()

    if args.verbose == 0:
        logging.basicConfig(level=logging.INFO, format='%(levelname)6s %(lineno)4s %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)6s %(lineno)4s %(message)s')

    d = TMIHWDriver()
    logger.info("Number channels: {}".format(d.num_channels()))
