#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging


class TestItem(object):

    # TODO: for html, consider this, https://github.com/Knio/dominate

    def __init__(self, ch_num, shared_state):
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, ch_num))
        self.chan = ch_num
        self.shared_state = shared_state

        self._record = None
        self.logger.info("DONE")

    # --------------------------------------------------------------------------
    # ------------ Script APIs wrapped by TestItem -----------------------------

    def log_bullet(self, text, ovrwrite_last_line=False):
        self.con.log_bullet(text, ovrwrite_last_line)

    def input_button(self, buttons, timeout=10):
        """ Create a row of buttons horizontally for user selection
        - each button entry looks like,
             {"value": "one",   "callback":"_TST005_button_handler", ["name": <unique_name>]}
        :param timeout: seconds
        :param buttons: list of button dicts
        :return {'success': True/False, 'button': <#>, ['err': <msg>]}
                where # is the index of the button selected by user
        """
        LOOPDELAY = 0.2
        loop_count = timeout / LOOPDELAY
        self.logger.info(buttons)
        return {'success': False, 'button': None, 'err': "Timeout"}

    def input_textbox(self, title, placeholder="", timeout=10):
        """ Create a textbox
        :param timeout: seconds
        :return {'success': True/False, 'textbox': <string>, ['err': <msg>]}

        TODO: regex feature.  Where to put the logic?
        """
        height = 60       # TODO: this is not exposed to the client yet, as single line only bokeh TextBox
        regex = None      # TODO: future regex feature... implement in JS in the test portal?

        self.shared_lock("__tmi_textbox_input__").acquire()

        LOOPDELAY = 0.2
        loop_count = timeout / LOOPDELAY
        tb = {"title": title, "placeholder": placeholder, "height": height, "regex": regex}
        self.logger.info(tb)

        return {'success': False, 'textbox': None, 'err': "Timeout"}

    def add_key(self, key, value, slot=None):
        """ Add keys to the suite test record
        - keys are things that the backend database would create keys on
        :param key:
        :param value:
        """
        self._record.add_key(key, value, slot)


    def shared_set_kv(self, key, value):
        self.shared_state.channel_set_kv(self.chan, key, value)

    def shared_get_kv(self, key):
        return self.shared_state.channel_get_kv(self.chan, key)

    def shared_lock(self, name):
        return self.shared_state.rsrc_lock_get(name)

    def shared_get_context(self):
        return self.shared_state.context_get(self.chan)

    def shared_get_drivers(self):
        return self.shared_state.get_drivers(self.chan)


