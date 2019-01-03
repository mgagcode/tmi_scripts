#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from core.tmi_test_item import TestItem
from public.station.api import ResultAPI


# file and class name must match
class pydso00xx(TestItem):

    DEMO_TIME_DELAY = 1.0
    DEMO_TIME_RND_ENABLE = 1

    def __init__(self, controller, chan, shared_state):
        super(pydso00xx, self).__init__(controller, chan, shared_state)
        self.logger = logging.getLogger("TMI.{}.{}".format(__name__, self.chan))
        self.dso = None

    def PYDSO0xxSETUP(self):
        ctx = self.item_start()  # always first line of test

        # drivers are stored in the shared_state and are retrieved as,
        drivers = self.shared_state.get_drivers(self.chan, type="AGILENT_DSO_USB_1")
        if len(drivers) > 1 or len(drivers) == 0:
            self.logger.error("Unexpected number of drivers: {}".format(drivers))
            self.log_bullet("Unexpected number of drivers")
            self.item_end(ResultAPI.RECORD_RESULT_INTERNAL_ERROR)
            return
        self.dso = drivers[0]['obj']["visa"]
        self.logger.info("Found dso: {}".format(self.dso))

        deets = self.dso.query('*IDN?')

        # save scope info
        _, _bullet = ctx.record.measurement("dso", deets, ResultAPI.UNIT_NONE)
        self.log_bullet(_bullet)

        self.item_end()  # always last line of test

    def PYDSO0xxTRDN(self):
        ctx = self.item_start()  # always first line of test

        self.item_end()  # always last line of test

