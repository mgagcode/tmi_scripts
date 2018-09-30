#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from core.tmi_test_item import TestItem
from public.api import ResultAPI
import time
from pubsub import pub
from random import randint, random
from drivers.micropythonbrd.tmi_micropython import TMIMicroPyBrd


class example1(TestItem):

    DEMO_TIME_DELAY_LOW = 1.0
    DEMO_TIME_DELAY_MED = 0.0
    DEMO_TIME_DELAY_HIGH = 0.0
    DEMO_TIME_RND_ENABLE = 0

    def __init__(self, controller, ch_num, shared_state):
        super(example1, self).__init__(controller, ch_num, shared_state)

        self.logger = logging.getLogger("TMI.{}.{}".format(__name__, ch_num))
        self.ch_num = ch_num
        self.log_module_begin("{}".format(__class__.__name__))

        # This script uses TMIHWDriver which has a driver with an ID, display
        # that id in the html log title and get the port for reference
        self.drivers = self.shared_state.get_drivers(ch_num)
        # we expect only one pyb driver, so index 0
        hwid = self.drivers[0].get("obj", {}).get("id", "ERROR")
        self.pyb_port = self.drivers[0].get("obj", {}).get("port", None)
        if self.pyb_port is "ERROR":
            self.logger.error("pyboard id could not be found")
            # TODO: raise exception?
        if self.pyb_port is None:
            self.logger.error("pyboard port could not be found")
            # TODO: raise exception?

        self.set_html_label("Channel {} - ID{}".format(ch_num, hwid))

        self.logger.info("ch {} pyb port {}".format(self.ch_num, self.pyb_port))

    # Override method
    # def onChanTool(self, item_dict, topic=pub.AUTO_TOPIC):
    #    self.logger.info("%r - %r" % (topic.getName(), item_dict))

    # Override method
    def onChanButton(self, item_dict, topic=pub.AUTO_TOPIC):
        self.logger.info("%r - %r" % (topic.getName(), item_dict))
        if item_dict["name"] == "DEBUG":
            self.ctlr._debug()

    def SETUP(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.guage_progress(5)

        self.pyb = TMIMicroPyBrd(logger=self.logger)
        self.pyb.open(self.pyb_port)
        self.item_end_PASS_helper() # always last line of test

    def TEARDOWN(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + randint(0, 10) / 10.0)

        cmds = ["pyb.LED(1).off()", "pyb.LED(2).off()", "pyb.LED(3).off()", "pyb.LED(4).off()"]
        cmd = "\n".join(cmds)
        self.pyb.execbuffer(cmd)

        self.pyb.close()
        self.guage_progress(100)
        self.item_end_PASS_helper() # always last line of test

    def TST000(self):
        context = self.item_start_helper()   # always first line of test

        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)

        # channel # delay to simulate a slower channel
        if self.ch_num == 0: time.sleep(1)

        cmds = ["pyb.LED(1).on()"]
        cmd = "\n".join(cmds)
        self.pyb.execbuffer(cmd)

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

    def TST001(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)

        cmds = ["pyb.LED(2).on()"]
        cmd = "\n".join(cmds)
        self.pyb.execbuffer(cmd)

        # example of skipping the next test item
        self.log_bullet("Skipping TST002", "blue")
        self.item_end_PASS_helper(_next="TST003")  # always last line of test

    def TST002(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        tst_str = "now is the time for all good men to come to the aid of their party"
        self.log_bullet(tst_str, "blue")
        _, _ = context["record"].record_test_add_measurement("string", tst_str, unit=ResultAPI.UNIT_STRING)
        self.item_end_PASS_helper()  # always last line of test

    def TST003(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)
        self.add_key("serial_num", "{}".format(randint(10000, 99999)))

        cmds = ["pyb.LED(3).on()"]
        cmd = "\n".join(cmds)
        self.pyb.execbuffer(cmd)

        _result, _bullet = context["record"].record_test_add_measurement("count",
                                                   randint(3, 15),
                                                   ResultAPI.UNIT_DB,
                                                   context["item"]["args"]["min"],
                                                   context["item"]["args"]["max"])
        self.log_bullet(_bullet)
        self.item_end_PASS_helper(item_result_state=_result)  # always last line of test

    def TST004(self):
        context = self.item_start_helper()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY_LOW + (randint(0, 10) / 10.0) * self.DEMO_TIME_RND_ENABLE)

        cmds = ["pyb.LED(4).on()"]
        cmd = "\n".join(cmds)
        self.pyb.execbuffer(cmd)

        # self.shared_state.channel_set_kv() can be used to send other channels
        # information...
        self.shared_set_kv("test", 321)
        self.item_end_PASS_helper()  # always last line of test

    def _TST005_button_handler(self, args):
        context = self.shared_state.info_get(self.ch_num)
        self.logger.info("%r" % args)
        self.shared_get_lock("text_entry").release()
        self.timeout_cancel()
        self.log_bullet(args["name"])

        # save the button that was pressed into shared state, so it can be retrieved later
        self.shared_set_kv( "button", args["name"])

        context["record"].record_test_add_measurement("button", args["name"], unit=ResultAPI.UNIT_STRING)
        self.item_end_PASS_helper()

    def TST005(self):
        """ Example of a user pressing one of a few different buttons
        """
        context = self.item_start_helper()  # always first line of test

        self.timeout_start(context["item"].get("timeout", 20))

        # grab a lock for user entry, else multiple channels will present
        # entry and user can be confused as to which one is focused
        self.shared_get_lock("text_entry").acquire()

        buttons = []
        buttons.append({"value": "one",   "callback": "_TST005_button_handler"})
        buttons.append({"value": "two",   "callback": "_TST005_button_handler"})
        buttons.append({"value": "three", "callback": "_TST005_button_handler"})
        self.log_input_button(buttons)

        # item_end_PASS_helper() is not called, but is required, the button callback
        # or the timeout timer callback will call the end helper for us.
        #self.item_end_PASS_helper()  # always last line of test

    def _TST006_handler(self, args):
        context = self.shared_state.info_get(self.ch_num)
        self.shared_get_lock("text_entry").release()
        self.logger.info("%r" % args)
        self.log_bullet(args["value"])
        context["record"].record_test_add_measurement(args["id"], args["value"], unit=ResultAPI.UNIT_STRING)
        self.item_end_PASS_helper()

    def TST006(self):
        context = self.item_start_helper()  # always first line of test

        # grab a lock for user entry, else multiple channels will present
        # entry and user can be confused as to which one is focused
        self.shared_get_lock("text_entry").acquire()
        self.log_input_text("tst006", "Your Name", "_TST006_handler")

    def _TST007_handler(self, args):
        context = self.shared_state.info_get(self.ch_num)
        self.text_entry_lock.release()
        self.logger.info("%r" % args)
        self.log_bullet(args["value"])
        context["record"].record_test_add_measurement(args["id"], args["value"], unit=ResultAPI.UNIT_STRING)
        self.item_end_PASS_helper()

    def TST007(self):
        context = self.item_start_helper()  # always first line of test

        self.shared_get_lock("text_entry").acquire()
        self.log_input_text("tst007", "Last", "_TST007_handler")

    def TST008(self):
        context = self.item_start_helper()  # always first line of test

        # shows how the guage works, two of them!
        self.log_bullet("Loading firmware...")
        self.log_guage_create("tst008_1")
        self.log_guage_create("tst008_2")
        for i in range(21):
            self.log_guage_set("tst008_1", i * 10)
            self.log_guage_set("tst008_2", (int(i * 5)))
            time.sleep(0.05)
            if i % 10 == 0: self.log_bullet("now i is {}".format(i))
        self.log_bullet("done")
        self.item_end_PASS_helper()

    def _TST_textinput_cb(self, args):
        # info_get pulls in test item context, so this
        # handler could service multiple test items
        context = self.shared_get_context(self.ch_num)
        self.logger.info("{}".format(args))
        self.log_bullet(str(args))
        self.log_bullet("{}".format(args['args']['dialog']['value']))
        self.item_end_PASS_helper()

    def TST009(self):
        context = self.item_start_helper()  # always first line of test
        args = {
            "title": "tst009",
            "instruction": "Test Type Anything",
            "regex": None,
            "value": "initial",
            "all_caps": True,
            "only_numbers": True,
            "cb": self._TST_textinput_cb,
        }
        self.log_input_text2(args)

    def TST010(self):
        context = self.item_start_helper()  # always first line of test
        args = {
            "title": "tst009",
            "instruction": "Enter Phone Number: ###-###-####",
            "regex": r"\w{3}-\w{3}-\w{4}$",
            "value": "###-###-####",
            "all_caps": True,
            "only_numbers": False,
            "cb": self._TST_textinput_cb,
        }
        self.log_input_text2(args)