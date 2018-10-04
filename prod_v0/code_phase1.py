#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from ...tmi.core.tmi_test_item import TestItem
from ...tmi.public.api import ResultAPI
import time
from random import randint, random


class code_phase1(TestItem):

    DEMO_TIME_DELAY_LOW = 1.0
    DEMO_TIME_DELAY_MED = 0.0
    DEMO_TIME_DELAY_HIGH = 0.0
    DEMO_TIME_RND_ENABLE = 0

    def __init__(self, controller, ch_num, shared_state):
        super(code_phase1, self).__init__(controller, ch_num, shared_state)

        self.logger = logging.getLogger("TMI.{}.{}".format(__name__, ch_num))
        self.ch_num = ch_num
        self.log_module_begin("{}".format(__class__.__name__))

        self.set_html_label("Channel {}".format(ch_num))
        self.logger.info("ch {}".format(self.ch_num))

    def SETUP(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.guage_progress(5)

        self.item_end_PASS_helper() # always last line of test

    def TEARDOWN(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + randint(0, 10) / 10.0)
        self.guage_progress(100)
        self.item_end_PASS_helper() # always last line of test

    def TST000(self):
        context = self.item_start_helper()   # always first line of test

        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)

        # channel # delay to simulate a slower channel
        if self.ch_num == 0: time.sleep(1)

        # example of taking multiple measurements, and sending as a list of results
        # if any test fails, this test item fails

        measurement_results = []
        _result, _bullet = context["record"].record_test_add_measurement("apples",
                                                   random(),
                                                   ResultAPI.UNIT_DB,
                                                   context["item"]["args"]["min"],
                                                   context["item"]["args"]["max"])
        self.log_bullet(_bullet)
        measurement_results.append(_result)

        _result, _bullet = context["record"].record_test_add_measurement("banannas",
                                                   randint(0, 10),
                                                   ResultAPI.UNIT_DB,
                                                   context["item"]["args"]["min"],
                                                   context["item"]["args"]["max"])
        self.log_bullet(_bullet)
        measurement_results.append(_result)

        self.item_end_PASS_helper(item_result_state=measurement_results) # always last line of test
