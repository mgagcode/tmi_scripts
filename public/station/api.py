#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018
"""

from app.const import Const


class ResultAPI(Const):

    RECORD_RESULT_UNKNOWN = "UNKNOWN" # this is an error if not changed
    RECORD_RESULT_PASS = "PASS"
    RECORD_RESULT_FAIL = "FAIL"
    RECORD_RESULT_TIMEOUT = "TIMEOUT"
    RECORD_RESULT_INCOMPLETE = "INC"
    RECORD_RESULT_INTERNAL_ERROR = "INTERNAL_ERROR"
    RECORD_RESULT_SKIP = "SKIP"
    RECORD_RESULT_DISABLED = "DISABLED"

    UNIT_OHMS = "Ohms"
    UNIT_DB = "dB"
    UNIT_VOLTS = "Volts"
    UNIT_CURRENT = "Amps"
    UNIT_STRING = "STR"
    UNIT_INT = "Integer"
    UNIT_FLOAT = "Float"
    UNIT_CELCIUS = "Celcius"
    UNIT_NONE = "None"

    TESTITEM_TIMEOUT = 10.0
