#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from pubsub import pub
from public.api import ResultAPI
from core.tmi_test_item import TestItem
import time
from random import randint, uniform


class code_phase2(TestItem):

    DEMO_TIME_DELAY_LOW = 1.0
    DEMO_TIME_DELAY_MED = 2.0
    DEMO_TIME_DELAY_HIGH = 3.0
    DEMO_TIME_RND_ENABLE = 0

    def __init__(self, controller, ch_num, shared_state):
        super(code_phase2, self).__init__(controller, ch_num, shared_state)

        self.logger = logging.getLogger("TMI.{}.{}".format(__name__, ch_num))
        self.ch_num = ch_num
        self.log_module_begin("{}".format(__class__.__name__))

        self.set_html_label("Channel {} - ID{}".format(ch_num, hwid))
        self.logger.info("ch {} pyb port {}".format(self.ch_num, self.pyb_port))

    # Overide method
    #def onChanTool(self, item_dict, topic=pub.AUTO_TOPIC):
    #    self.logger.info("%r - %r" % (topic.getName(), item_dict))

    # Overide method
    def onChanButton(self, item_dict, topic=pub.AUTO_TOPIC):
        self.logger.info("%r - %r" % (topic.getName(), item_dict))
        if item_dict["name"] == "DEBUG":
            self.ctlr._debug()

    def SETUP(self):
        info = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.guage_progress(5)
        self.item_end_PASS_helper()  # always last line of test

    def TEARDOWN(self):
        info = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + randint(0, 10) / 10.0)
        self.guage_progress(100)
        self.item_end_PASS_helper()  # always last line of test

    def TST000(self):
        info = self.item_start_helper()   # always first line of test

        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        if self.ch_num == 0: time.sleep(1)

        measurement_results = []
        _result, _bullet = info["record"].record_test_add_measurement(
                "apples", uniform(0, 1.01), ResultAPI.UNIT_DB, info["item"]["args"]["min"], info["item"]["args"]["max"])
        measurement_results.append(_result)
        self.log_bullet(_bullet)

        _result, _bullet = info["record"].record_test_add_measurement(
                "banannas", uniform(0, 1.01), ResultAPI.UNIT_DB, info["item"]["args"]["min"], info["item"]["args"]["max"])
        measurement_results.append(_result)
        self.log_bullet(_bullet)

        self.item_end_PASS_helper(item_result_state=measurement_results) # always last line of test

    def TST001(self):
        info = self.item_start_helper()  # always first line of test

        # print out which button was pressed...
        success, button = self.shared_get_kv("button")
        if not success: button = "NOT FOUND"
        self.log_bullet("button pressed was {}".format(button))

        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.item_end_PASS_helper()  # always last line of test

    def TST002(self):
        info = self.item_start_helper()  # always first line of test

        # example of use a resource lock
        self.log_bullet("waiting for lock...")
        with self.shared_get_lock("fox"):
            self.log_bullet("got the lock, working...")
            time.sleep(self.DEMO_TIME_DELAY_LOW)
            str = "the quick brown fox jumped over the lazy dog back"
            self.log_bullet(str, "blue")
            time.sleep(self.DEMO_TIME_DELAY_MED)
        self.log_bullet("released the lock!")

        info["record"].record_test_add_measurement("string", str, unit=ResultAPI.UNIT_STRING)
        self.item_end_PASS_helper()  # always last line of test

    def TST003(self):
        info = self.item_start_helper()  # always first line of test

        # print out which button was pressed...
        success, button = self.shared_get_kv("test")
        if not success: button = "NOT FOUND"
        self.log_bullet("test value {}".format(button))

        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.item_end_PASS_helper()  # always last line of test

    def TST004(self):
        info = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.item_end_PASS_helper()  # always last line of test