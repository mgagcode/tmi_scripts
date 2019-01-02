#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from pubsub import pub
from app.const import TMI_PUB
import visa

class TMIHWDriver(object):
    """
    Create a single instance of an Agilent DSO of "type 1"
    - presumably most Agolent scopes are compatible with each other...
    - those that are compatible can share the same driver...(presumably)
    - this driver supports USB attached devices
    """

    DRIVER_TYPE = "AGILENT_DSO_USB_1"

    def __init__(self, shared_state):
        self.logger = logging.getLogger("TMI.{}".format(__class__.__name__))
        self.logger.info("Start")
        self.shared_state = shared_state
        self.pybs = []
        self._num_chan = -1  # indicates this device does not set channels

    def discover_channels(self):

        dd = {"notice": "TMIHWDriver: Scanning for {}".format(DRIVER_TYPE),
              "from": "{}:{}".format(__class__.__name__, "discover_channels")}
        pub.sendMessage(TMI_PUB.TMI_FRAME_SYSTEM_NOTICE, item_dict=dd)

        rm = visa.ResourceManager()
        dso_agilent_dso7104b_list = rm.list_resources(query='USB?::2391::5981::?*::?*::INSTR')

        self._num_chan = len(self.pybs)
        self.shared_state.add_drivers(self.DRIVER_TYPE, self.pybs)

        dd = {"notice": "TMIHWDriver: Found {}!".format(self._num_chan),
              "from": "{}".format(__class__.__name__)}
        pub.sendMessage(TMI_PUB.TMI_FRAME_SYSTEM_NOTICE, item_dict=dd)
        self.logger.info("Done")
        return self._num_chan

    def num_channels(self):
        return self._num_chan

    def init_play_pub(self):
        """ Function to instantiate a class/thread to trigger PLAY of script
        """
        self.logger.info("{} does not support 'play' messaging".format(self.DRIVER_TYPE))
