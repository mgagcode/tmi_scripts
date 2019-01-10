#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018-2019

"""
import os
import logging
import threading
import time
from public.station.drivers.micropythonbrd.list_serial import serial_ports
from public.station.drivers.micropythonbrd.tmi_upybrd import TMIMicroPyBrd

from pubsub import pub
from app.const import TMI_PUB, TMI_CHANNEL
from app.sys_log import pub_notice

class upybrdPlayPub(threading.Thread):
    """ Creates a thread per channel that will poll the switch
    on the upybrd, and if it is pressed, will pub the PLAY msg to
    start testing on that port.

    TODO: handle Pass/Fail LED indication at the end of the test...

    """
    POLL_TIMER_SEC = 1

    def __init__(self, ch, drv):
        super(upybrdPlayPub, self).__init__()
        self._stop_event = threading.Event()
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, ch))

        self.ch = ch
        self.pyb_port = drv["obj"]["port"]
        self.pyb = TMIMicroPyBrd(loggerIn=self.logger)
        self.ch_state = TMI_CHANNEL.STATE_UNKNOWN
        self.ch_pub = TMI_PUB.get_tmi_channel_num_play(ch)
        self.open_fixture = False  # assume fixture is closed

        pub.subscribe(self.onTMI_SHUTDOWN, TMI_PUB.TMI_SHUTDOWN)
        pub.subscribe(self.onTMI_CHANNEL_STATE, TMI_PUB.TMI_CHANNEL_STATE)

        self.start()

    def _unsubscribe(self):
        pub.unsubscribe(self.onTMI_SHUTDOWN, TMI_PUB.TMI_SHUTDOWN)
        pub.subscribe(self.onTMI_CHANNEL_STATE, TMI_PUB.TMI_CHANNEL_STATE)

    def shutdown(self):
        self._stop_event.set()
        self.join()
        self._unsubscribe()

    def close(self):
        self.shutdown()

    def onTMI_SHUTDOWN(self, item_dict, topic=pub.AUTO_TOPIC):
        self.logger.info("{} - {}".format(topic.getName(), item_dict))
        self.shutdown()

    def onTMI_CHANNEL_STATE(self, item_dict, topic=pub.AUTO_TOPIC):
        # {"ch": #, "state": <state>, "from": 'TMIChanCon'}
        if item_dict["ch"] != self.ch: return
        self.logger.info("%r - %r" % (topic.getName(), item_dict))
        self.ch_state = item_dict["state"]

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        pub_play = False
        while not self.stopped():
            time.sleep(self.POLL_TIMER_SEC)
            if self.ch_state in [TMI_CHANNEL.STATE_DONE, TMI_CHANNEL.STATE_READY]:
                self.pyb.open(self.pyb_port)

                cmds = ["from pyb import Pin",
                        "p_in = Pin('X1', Pin.IN, Pin.PULL_UP)",
                        "print(p_in.value())",
                        ]
                cmd = "\n".join(cmds).strip()
                success, result = self.pyb.execbuffer(cmd)
                self.logger.debug("{}, {}".format(success, result))
                if success:
                    # only if the fixture was in the previously opened state, then we play
                    # in other words, once lid is closed, it must be opened again to trigger play
                    if self.open_fixture and result.strip() == "0":
                        pub_play = True
                        self.open_fixture = False
                        self.logger.info("Channel {} PLAY".format(self.ch))
                    elif result.strip() == "1":
                        self.open_fixture = True

                else:
                    pub_play = False

                self.pyb.close()

                self.logger.info("open_fixture: {}, play: {}".format(self.open_fixture, pub_play))
                if pub_play:
                    pub_play = False
                    d = {"channels": [self.ch], "from": "TMI.{}.{}".format(__class__.__name__, self.ch)}
                    pub.sendMessage(self.ch_pub, item_dict=d)

        self.logger.info("!!! run loop stopped !!!")


class TMIHWDriver(object):
    """
    Determine MicroPyBoards attached to the system, and report them to
    the system shared state.
    """
    SFN = os.path.basename(__file__)

    DRIVER_TYPE = "TMIMicroPyBrd"

    def __init__(self, shared_state):
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, self.SFN))
        self.logger.info("Start")
        self.shared_state = shared_state
        self.pybs = []
        self._num_chan = 0

    def discover_channels(self):
        """ determine the number of channels, and populate hw drivers into shared state

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
        sender = "{}.{}".format(self.SFN, __class__.__name__)

        ports = serial_ports()

        pub_notice("TMIHWDriver: Scanning for MicroPyBoards on {}".format(ports), sender=sender)

        self.pybs.clear()
        pyboard = TMIMicroPyBrd(self.logger)
        for port in ports:
            pyb = pyboard.scan_ports(port)

            # pyb will be a list of dicts, since we sent in the port to scan,
            # there will be only one item in the list, thus index [0].
            #   [{"port": port, "id": id, "version": TMI_VERSION}]
            # TODO: could not set port, and get the list of ports in one go...

            if not pyb:
                self.logger.info("port {} -> Nothing found".format(port))
                continue

            if pyb[0].get('id', None) is None:
                self.logger.info("port {} -> Missing ID".format(port))
                continue

            # divers can register a close() method which is called on channel destroy.
            # we don't need to set that there is none, but doing so helps remember we could set one
            pyb[0]["close"] = False

            self.pybs.append(pyb[0])
            msg = "TMIHWDriver:{}: {} -> {}".format(self.SFN, port, pyb[0])

            self.logger.info(msg)
            pub_notice(msg, sender=sender)

        pyboard.close()

        self._num_chan = len(self.pybs)
        self.shared_state.add_drivers(self.DRIVER_TYPE, self.pybs)

        pub_notice("TMIHWDriver:{}: Found {}!".format(self.SFN, self._num_chan), sender=sender)
        self.logger.info("Done: {} channels".format(self._num_chan))
        return self._num_chan

    def num_channels(self):
        return self._num_chan

    def init_play_pub(self):
        """ Function to instantiate a class/thread to trigger PLAY of script
        - this is called right after discover_channels
        """
        self.logger.info("Creating...")

        # Note that channels are mapped to 'id' in ascending order, which is done
        # by self.shared_state.add_drivers(), so to get the order right, we need to
        # get the drivers from self.shared_state.get_drivers()

        for ch in range(self._num_chan):
            drivers = self.shared_state.get_drivers(ch, type=self.DRIVER_TYPE)
            # there should only be one driver of our type!
            # TODO: move this check to shared_state
            if len(drivers) > 1:
                self.logger.error("Unexpected number of drivers: {}".format(drivers))
                continue

            self.logger.info("Adding 'play' support on channel {}".format(ch))
            play_pub = upybrdPlayPub(ch, drivers[0])
            d = {"id": ch, "obj": play_pub, "close": play_pub.close}
            self.shared_state.add_drivers("upybrdPlayPub", [d])
