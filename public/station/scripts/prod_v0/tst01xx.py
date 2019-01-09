#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018-2019

"""
import logging
from core.tmi_test_item import TestItem
from public.station.api import ResultAPI
import time
from random import randint, random


# file name and class name must match
class tst01xx(TestItem):

    DEMO_TIME_DELAY = 1.0
    DEMO_TIME_RND_ENABLE = 1

    def __init__(self, controller, chan, shared_state):
        super().__init__(controller, chan, shared_state)
        self.logger = logging.getLogger("TMI.{}.{}".format(__name__, self.chan))

    def TST1xxSETUP(self):
        context = self.item_start()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        self.item_end() # always last line of test

    def TST1xxTRDN(self):
        context = self.item_start()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)
        self.item_end() # always last line of test

    def TST100_Meas(self):
        """ Example test

        {"id": "TST100_Meas", "enable": true,  "args": {"min": 0, "max": "%%TST100Max"},
                      "fail": [ {"fid": "TST100-0", "msg": "Component R1"} ] },
        """
        ctx = self.item_start()   # always first line of test

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        # example of taking multiple measurements, and sending as a list of results
        # if any test fails, this test item fails
        # This test has a failure message in the script, depending on the failure mode,
        #"fail": [ {"fid": "TST100-0", "msg": "Component R1"} ] }
        FAIL_ID = 0

        measurement_results = []
        _result, _bullet = ctx.record.measurement("apples",
                                                  random(),
                                                  ResultAPI.UNIT_DB,
                                                  ctx.item.args.min,
                                                  ctx.item.args.max)
        # set the failure msg on failure
        if _result == ResultAPI.RECORD_RESULT_FAIL:
            msg = ctx.item.fail[FAIL_ID]
            ctx.record.fail_msg(msg)

        self.log_bullet(_bullet)
        measurement_results.append(_result)

        _result, _bullet = ctx.record.measurement("bananas",
                                                  randint(0, 10),
                                                  ResultAPI.UNIT_DB,
                                                  ctx.item.args.min,
                                                  ctx.item.args.min)

        # set the failure msg on failure
        if _result == ResultAPI.RECORD_RESULT_FAIL:
            msg = ctx.item.fail[FAIL_ID]
            ctx.record.fail_msg(msg)

        self.log_bullet(_bullet)
        measurement_results.append(_result)

        self.item_end(item_result_state=measurement_results) # always last line of test

    def TST101_Skip(self):
        """ Example of a test that is skipped

        {"id": "TST001_Skip", "enable": false },

        """
        ctx = self.item_start()   # always first line of test
        # this is a skipped test for testing, in some scripts

        self.log_bullet("Was I skipped?")

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        self.item_end() # always last line of test

