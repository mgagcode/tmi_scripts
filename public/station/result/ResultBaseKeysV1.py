#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from core.resultBaseClass import ResultBaseClass


class ResultBaseKeysV1(ResultBaseClass):
    """ ResultBaseKeysV1

    This result extends the base class with a "keys" section.
    "keys" are meant to hold things like serial numbers, password keys, etc from the product.

    The DB record holds key0, key1, key2, .. up to key{}.format(MAX_KEYS).
    The idea is that these keys would be mapped for specific purposes, and thus
    these key#s can serve arbitrary purposes.  One could have given these keys specific
    names, rather than an abstract key#.

    The final dict will look like this: ["keys"]["key#"] = "{}:{}".format(key:value)
    """
    MAX_KEYS = 4

    def __init__(self, chan_num, operator="UNKNOWN", script_filename="UNKNOWN"):
        super().__init__(chan_num, operator, script_filename)

        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, chan_num))

        # The ResultBaseClass meta processor must be changed
        self._record["meta"]["processor"] = __class__.__name__

        # "keys" is extension of ResultBaseClass
        self._record["keys"] = {}

        self.logger.info("DONE")

    def add_key(self, key, value, slot=None):
        """ Adds a key value pair into a key# "slot"

        The final dict will look like this: ["keys"]["key#"] = "{}:{}".format(key:value)

        :param key:
        :param value:
        :param slot: if not specified, the next available slot is used
        :return: True if succeeded, False otherwise
        """
        if slot is None:
            num_keys = len(self._record["keys"])
            if num_keys >= self.MAX_KEYS:
                self.logger.error("recorded has exceeded maximum keys")
                return False

            # find the next empty slot (key#) and insert the key:value
            for i in range(self.MAX_KEYS):
                if not "key{}".format(i) in self._record["keys"]: break
            self._record["keys"]["key{}".format(i)] = key + ":" + str(value)

        else:
            if slot >= self.MAX_KEYS:
                self.logger.error("recorded has exceeded maximum keys")
                return False
            self._record["keys"]["key{}".format(slot)] = key + ":" + str(value)

        return True

    def get_keys(self):
        return self._record["keys"]
