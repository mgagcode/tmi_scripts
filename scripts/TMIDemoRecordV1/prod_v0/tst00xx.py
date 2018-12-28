#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from core.tmi_test_item import TestItem
from public.api import ResultAPI
import time
from random import randint, random


# file and class name must match
class tst00xx(TestItem):

    DEMO_TIME_DELAY = 1.0
    DEMO_TIME_RND_ENABLE = 1

    def __init__(self, controller, ch_num, shared_state):
        super(tst00xx, self).__init__(controller, ch_num, shared_state)
        self.logger = logging.getLogger("TMI.{}.{}".format(__name__, self.chan))

        # ------------------------------------------------------------------------
        # API Reference
        #
        # ctx = self.item_start()  # always first line of test
        #  - use ctx (context) to extract information to drive the test program
        #  - ctx (context) is a namespace of content from the test script
        #  - ctx.item = {"id": "TST000", "enable": True,  "args": {"min": 0, "max": 10}}
        #  - ctx.item.args = {"min": 0, "max": 10}
        #  - ctx.item.args.max = 10
        #  - ctx.options = { "fail_fast": False }
        #  - ctx.options.fail_fast = False
        #
        #  - record functions
        #    - ctx.record.measurement(name, value, unit, min=None, max=None)
        #      - name: name of the measurement, should be unique per test item
        #      - unit: from ResultAPI.UNIT_*
        #    - result extensions
        #      - the result base class can be extended, as it has in this example
        #      - class TMIDemoRecordV1(ResultBaseClass)
        #      - two functions were added, and used in this example,
        #        - add_key(key, value, slot=None)
        #        - get_keys()
        #
        # self.chan  # this channel
        #
        # self.item_end([result[s]]) # always last line of test
        #  - result is one of ResultAPI.RECORD_* constants
        #  - result may be a list or a single instance
        #  - called without arguments, the result is ResultAPI.RECORD_RESULT_PASS
        #
        # Usage Reference
        #
        # 1) Test Item Timeout
        #    - every test time is guarded by a timeout which has a default of ResultAPI.TESTITEM_TIMEOUT Sec.
        #    - this value can be overridden by adding '"timeout": <value>' to the test item in the script
        #    - if the timeout expires, it is considered an internal crash, even if it is
        #      on a user input item.  The test script will fail, and a crash report is generated.
        #

    def TST0xxSETUP(self):
        ctx = self.item_start()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        self.item_end()  # always last line of test

    def TST0xxTRDN(self):
        ctx = self.item_start()  # always first line of test
        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)
        self.item_end()  # always last line of test

    def TST000_Meas(self):
        """ Measurement example, with multiple failure messages
        - example of taking multiple measurements, and sending as a list of results
        - if any test fails, this test item fails

            {"id": "TST000_Meas",    "enable": true, "args": {"min": 0, "max": 10},
                                     "fail": [ {"fid": "TST000-0", "msg": "Component apple R1"},
                                               {"fid": "TST000-1", "msg": "Component banana R1"}] },
        :return:
        """
        ctx = self.item_start()   # always first line of test

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        FAIL_APPLE   = 0  # indexes into the "fail" list, just for code readability
        FAIL_BANANNA = 1

        measurement_results = []  # list for all the coming measurements...

        # Apples measurement...
        _result, _bullet = ctx.record.measurement("apples",
                                                  random(),
                                                  ResultAPI.UNIT_DB,
                                                  ctx.item.args.min,
                                                  ctx.item.args.max)
        # if failed, there is a msg in script to attach to the record, for repair purposes
        if _result == ResultAPI.RECORD_RESULT_FAIL:
            msg = ctx.item.fail[FAIL_APPLE]
            ctx.record.fail_msg(msg)

        self.log_bullet(_bullet)
        measurement_results.append(_result)

        # Bananas measurement...
        _result, _bullet = ctx.record.measurement("bananas",
                                                  randint(0, 10),
                                                  ResultAPI.UNIT_DB,
                                                  ctx.item.args.min,
                                                  ctx.item.args.max)

        # if failed, there is a msg in script to attach to the record, for repair purposes
        if _result == ResultAPI.RECORD_RESULT_FAIL:
            msg = ctx.item.fail[FAIL_BANANNA]
            ctx.record.fail_msg(msg)

        self.log_bullet(_bullet)
        measurement_results.append(_result)

        # Note that we can send a list of measurements
        self.item_end(item_result_state=measurement_results)  # always last line of test

    def TST001_Skip(self):
        ctx = self.item_start()   # always first line of test
        # this is a skipped test for testing, in some scripts

        self.log_bullet("Was I skipped?")

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        self.item_end()  # always last line of test

    def TST002_Buttons(self):
        """ Select one of three buttons
        - capture the button index in the test record
        """
        ctx = self.item_start()   # always first line of test

        self.log_bullet("Please press a button!")

        buttons = ["one", "two", "three"]
        user_select = self.input_button(buttons)
        if user_select["success"]:
            b_idx = user_select["button"]
            self.log_bullet("{} was pressed!".format(buttons[b_idx]))
            _result, _bullet = ctx.record.measurement("button", b_idx, ResultAPI.UNIT_INT)
            self.log_bullet(_bullet)
        else:
            _result = ResultAPI.RECORD_RESULT_FAIL
            self.log_bullet(user_select.get("err", "UNKNOWN ERROR"))

        self.item_end(_result)  # always last line of test

    def TST003_KeyAdd(self):
        """ How use of keys: keys are things like serial numbers.
        - every call to self.add_key(k,v) adds the "k:v" to the next available
          key# in the record, you can force the slot though.  It depends how you will
          manage the keys in the final database; either by convention force every slot
          to represent a specific thing (preferred), or search all keys for the 'k' you want.
        :return:
        """
        ctx = self.item_start()   # always first line of test

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        value = randint(0, 100)
        ctx.record.add_key("value", value, slot=0)
        self.log_bullet("added key value: {}".format(value))

        self.item_end()  # always last line of test

    def TST004_KeyGet(self):
        """ How use of keys works
        - retrieve a previous key, otherwise fail test
        """
        ctx = self.item_start()  # always first line of test

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        keys = ctx.record.get_keys()
        if not keys.get("key0", False):
            self.log_bullet("ERROR key[0]: {}".format("NOT FOUND!"))
            self.item_end(ResultAPI.RECORD_RESULT_FAIL)  # always last line of test
            return

        self.log_bullet("got key[0]: {}".format(keys.get("key0", "NOT FOUND!")))
        self.item_end()  # always last line of test

    def TST005_RsrcLock(self):
        """ Demonstrate locking of a resource in shared_state
        - lock a resource for some time, and then release
        - this is useful for a piece of test equipment that is shared across channels
        """
        ctx = self.item_start()  # always first line of test

        hold_time = ctx.item.args.get("holdTime", 5)

        self.log_bullet("waiting for my_resource...")
        self.shared_lock("my_resource").acquire()
        while hold_time:
            self.log_bullet("my_resource is locked for {} seconds".format(hold_time), ovrwrite_last_line=True)
            time.sleep(1)
            hold_time -= 1
        self.shared_lock("my_resource").release()
        self.log_bullet("my_resource is free")

        self.item_end()  # always last line of test

    def TST006_HWDriver(self):
        """ How to get a driver that was initialized when script was loaded
        - when the script is loaded, HW driver are initialized and stored in the shared
          state.  The format of the return data is,

          {"channel": idx, "type": type, "obj": d}
          where d:  {'id': <int>, "version": <version>, <"key": "value">, ...}

        - how the "obj" field depends on the HW driver
        """
        ctx = self.item_start()  # always first line of test

        time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)

        drivers = self.shared_get_drivers()
        for driver in drivers:
            self.log_bullet("found driver: {} {} {}".format(driver["type"],
                                                            driver["obj"]["id"],
                                                            driver["obj"]["version"]))

        self.item_end()  # always last line of test

    def TST007_LogPctProgress(self):
        """ Demo a log bullet with increasing percent
        """
        ctx = self.item_start()  # always first line of test

        percent = 0
        while percent <= 100:
            bar = "#" * int(40 * percent / 100)
            msg = "Completed {:3d}% {}".format(percent, bar)
            self.log_bullet(msg, ovrwrite_last_line=True)
            time.sleep(self.DEMO_TIME_DELAY * random() * self.DEMO_TIME_RND_ENABLE)
            percent += 10

        self.item_end()  # always last line of test

    def TST008_TextInput(self):
        """ Text Input Box
        """
        ctx = self.item_start()   # always first line of test

        self.log_bullet("Please Enter Text!")

        user_text = self.input_textbox("Enter Some Text:", "change")
        if user_text["success"]:
            self.log_bullet("Text: {}".format(user_text["textbox"]))

            # qualify the text here, and either if the text is invalid, re-ask
            # make sure you don't timeout...

            _result = ResultAPI.RECORD_RESULT_PASS
        else:
            _result = ResultAPI.RECORD_RESULT_FAIL
            self.log_bullet(user_text.get("err", "UNKNOWN ERROR"))

        self.item_end(_result)  # always last line of test
