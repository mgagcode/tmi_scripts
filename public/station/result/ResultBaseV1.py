#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import logging
from core.resultBaseClass import ResultBaseClass


class ResultBaseV1(ResultBaseClass):
    """ ResultBaseV1
    - basic record type, no extensions
    """
    def __init__(self, chan_num, operator="UNKNOWN", script_filename="UNKNOWN"):
        super().__init__(chan_num, operator, script_filename)
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, chan_num))
        # The ResultBaseClass meta processor must be changed
        self._record["meta"]["processor"] = __class__.__name__
        self.logger.info("DONE")
