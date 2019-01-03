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
    - See https://pyvisa.readthedocs.io/en/1.8/names.html
    - SB[board]::manufacturer ID::model code::serial number[::USB interface number][::INSTR]
    - DSO Agilent DSO7104B, returns ('USB0::2391::5981::MY49520121::0::INSTR',)
    - therefore, assuming 2391::5981, means Agilent DSO7000 series (?)
    - query('*IDN?') returns
        AGILENT TECHNOLOGIES,DSO7104B,MY49520121,06.00.0003
    """
    TMI_VERSION = "0.0.1"
    DRIVER_TYPE = "AGILENT_DSO_USB_1"
    # list of DSOs that accept the same command set
    WHITE_LIST = ["DSO7104B"]

    def __init__(self, shared_state):
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, self.DRIVER_TYPE))
        self.logger.info("Start")
        self.shared_state = shared_state
        self.pybs = []
        self._num_chan = -1  # indicates this device does not set channels

    def discover_channels(self):
        """ determine the number of channels, and popultae hw drivers into shared state

        shared_state: a list,
            self.shared_state.add_drivers(DRV_TYPE, [ {}, {}, ... ])

        [ {'id': i,               # id of the channel
           "version": <VERSION>,  # version of the driver
           "close": False},       # register a callback on closing the channel
           "<foo>": <bar>,        # something that makes your HW work...
        ]

        :return: >0 number of channels,
                  0 does not indicate num channels, like a shared hardware driver
                 <0 error
        """
        dd = {"notice": "TMIHWDriver: Scanning for {}".format(self.DRIVER_TYPE),
              "from": "{}:{}".format(__class__.__name__, "discover_channels")}
        pub.sendMessage(TMI_PUB.TMI_FRAME_SYSTEM_NOTICE, item_dict=dd)

        rm = visa.ResourceManager()
        dso_agilent_usb_list = rm.list_resources(query='USB?::2391::5981::?*::?*::INSTR')

        # find the first scope
        found = False
        instr = None
        for dso in dso_agilent_usb_list:
            instr = rm.open_resource(dso)
            deets = instr.query('*IDN?').strip()
            for scope in self.WHITE_LIST:
                if scope in deets:
                    found = True
                    break

            if found: break

        self.logger.info("found: {} {}".format(found, deets))

        if not found:
            dd = {"notice": "TMIHWDriver: none found", "from": "{}.{}".format(__class__.__name__, self.DRIVER_TYPE)}
            pub.sendMessage(TMI_PUB.TMI_FRAME_SYSTEM_NOTICE, item_dict=dd)
            return -1

        d = {
            "id": 0,
            "version": self.TMI_VERSION,
            "close": False,
            "visa": instr,
        }

        self.shared_state.add_drivers(self.DRIVER_TYPE, [d], shared=True)

        dd = {"notice": "TMIHWDriver: Found {}!".format(instr), "from": "{}".format(__class__.__name__)}
        pub.sendMessage(TMI_PUB.TMI_FRAME_SYSTEM_NOTICE, item_dict=dd)
        self.logger.info("Done")

        # by returning 0, it means this return values DOES not represent number of channels
        return 0

    def num_channels(self):
        return self._num_chan

    def init_play_pub(self):
        """ Function to instantiate a class/thread to trigger PLAY of script
        - this is called right after discover_channels
        """
        self.logger.info("{} does not support 'play' messaging".format(self.DRIVER_TYPE))
