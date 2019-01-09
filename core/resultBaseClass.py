#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018-2019

"""
import os
import time
import logging
import datetime
import platform
import json
import uuid
from public.station.api import ResultAPI


class ResultBaseClass(object):
    """
    Base Result Record for the whole test suite

    """

    EPOCH_DECIMAL_PLACES = 2
    SECRET_KEY = "TMIDemoRecordV1_secret"  # public encryption key

    def __init__(self, chan_num, operator="UNKNOWN", script_filename=None):
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, chan_num))

        self._record = {    ## The result json record for the suite
            "meta": { # stuff that framework populates
                      "channel": chan_num,
                      "result": ResultAPI.RECORD_RESULT_UNKNOWN,
                      "processor": __class__.__name__,
                      "operator": operator,
                      "ip": "127.0.0.1",
                      "script": os.path.normpath(script_filename).replace("\\", "/"),
                    },
            "info": {},      # stuff customer populates
            "config": {},    # copied from the script input
            "items": [],     # list of results, see Result class
            "errors": [],    # list of errors, for crash logs
            "html_summary": None,
        }
        self._item = {}
        self.logger.info("DONE")

    def record_add_error(self, msg):
        if isinstance(msg, list):
            for m in msg:
                self._record["errors"].append(m)
        else:
            self._record["errors"].append(msg)

    def record_item_create(self, name):
        self._item = {
            "name": name,
            "result": ResultAPI.RECORD_RESULT_UNKNOWN,
            "timestamp_start": round(time.time(), self.EPOCH_DECIMAL_PLACES),
            "timestamp_end": 0,
            "measurements": [],
            "fail_msg": {}  # like {"fid": "TST000-0", "msg": "Component R1"}
        }

    def record_meta_set_result(self, _result):
        self._record["meta"]["result"] = _result

    def record_meta_get_result(self):
        return self._record["meta"]["result"]

    def record_meta_get_duration(self):
        end = datetime.datetime.strptime(self._record["meta"]["end"], "%Y-%m-%dT%H:%M:%S.%f")
        start = datetime.datetime.strptime(self._record["meta"]["start"], "%Y-%m-%dT%H:%M:%S.%f")
        return (end - start).total_seconds()

    def record_test_set_result(self, _result):
        """
        :param _result: one of ResultAPI.RECORD_RESULT_*
        :return:
        """
        self._item["result"] = _result

        if self.record_meta_get_result() == ResultAPI.RECORD_RESULT_UNKNOWN:
            self.record_meta_set_result(_result)
        elif self.record_meta_get_result() == ResultAPI.RECORD_RESULT_PASS:
            self.record_meta_set_result(_result)
        elif self.record_meta_get_result() == ResultAPI.RECORD_RESULT_FAIL:
            pass
        else:
            self.record_meta_set_result(_result)

    def record_test_get_result(self):
        return self._item["result"]

    def record_test_get_duration(self):
        return self._item["timestamp_end"] - self._item["timestamp_start"]

    def record_item_end(self):
        self._item["timestamp_end"] = round(time.time(), self.EPOCH_DECIMAL_PLACES)
        self._record["items"].append(self._item)

    def record_items_get(self):
        return self._record["items"]

    def measurement(self, name, value, unit, min=None, max=None):
        """
        :param name:
        :param min:
        :param max:
        :param value:
        :param unit: one of self.UNIT_*
        :return: True if value within limits, otherwise False
                 string, string of test
        """
        _pass = ResultAPI.RECORD_RESULT_UNKNOWN

        d = {
            "name": "{}.{}".format(self._item["name"], name),
            "unit": unit,
        }

        if isinstance(min, (int, float)) and isinstance(max, (int, float)) and isinstance(value, (int, float)):
            if min <= value <= max: _pass = ResultAPI.RECORD_RESULT_PASS
            else: _pass = ResultAPI.RECORD_RESULT_FAIL
            d["min"] = "{:32.16}".format(str(float(min))).rstrip()
            d["max"] = "{:32.16}".format(str(float(max))).rstrip()
            d["value"] = "{:64.16}".format(str(float(value))).rstrip()
            self.logger.debug("{} <= {} <= {} : {}".format(d["min"], d["value"], d["max"], _pass))
        elif min is None and max is None and isinstance(value, (int, float, str)):
            _pass = ResultAPI.RECORD_RESULT_PASS
            d["min"] = None
            d["max"] = None
            if unit == ResultAPI.UNIT_INT:
                d["value"] = int(value)
            elif unit == ResultAPI.UNIT_FLOAT:
                d["value"] = float(value)
            elif unit == ResultAPI.UNIT_STRING:
                d["value"] = "{}".format(value)
            elif isinstance(value, (int, )):
                d["value"] = "{}".format(int(value))
            elif isinstance(value, (float)):
                d["value"] = "{:64.16}".format(str(float(value))).rstrip()
            elif isinstance(value, str):
                d["value"] = "{:64}".format(value).rstrip()
            self.logger.debug("{} <= {} <= {} : {}".format(d["min"], d["value"], d["max"], _pass))
        else:
            _pass = ResultAPI.RECORD_RESULT_INTERNAL_ERROR
            self.logger.error("{} <= {} <= {} : {}".format(min, value, max, _pass))

        d["result"] = _pass

        self._item["measurements"].append(d)
        _bullet = "{}: {} <= {} <= {} {} :: {}".format(name, d["min"], d["value"], d["max"], unit, _pass)
        self.logger.info(d)
        return _pass, _bullet

    def fail_msg(self, fail_msg):
        if isinstance(fail_msg, dict):
            self._item["fail_msg"] = fail_msg
            self.logger.info(fail_msg)
        else:
            self.logger.error("expected dict for fail_msg")

    def record_item_get(self): return self._item

    def __meta_add(self, m):
        self._record["meta"] = {**self._record["meta"], **m}

    def record_record_meta_init(self):
        _meta = {
            "version": "TBD-framework version",
            "start": datetime.datetime.utcnow().isoformat(),
            "end": "",
            "hostname": [i for i in platform.uname()],
            "result": ResultAPI.RECORD_RESULT_UNKNOWN,
        }
        self.__meta_add(_meta)

    def record_record_meta_fini(self, state=None):
        if state is None:
            _state = ResultAPI.RECORD_RESULT_PASS
            for test in self._record["items"]:
                if test["result"] in [ResultAPI.RECORD_RESULT_FAIL,
                                      ResultAPI.RECORD_RESULT_TIMEOUT,
                                      ResultAPI.RECORD_RESULT_UNKNOWN,
                                      ResultAPI.RECORD_RESULT_INCOMPLETE]:
                    _state = ResultAPI.RECORD_RESULT_FAIL
        else:
            _state = state
        _meta = {
            "end": datetime.datetime.utcnow().isoformat(),
            "result": _state,
        }
        self.__meta_add(_meta)

    def record_record_meta_set(self, _meta):
        self.__meta_add(_meta)

    def record_info_set(self, _info_dict):
        self._record["info"] = {**self._record["info"], **_info_dict}

    def record_record_html_summary(self, summary):
        """ Add View Log Summary to the record.  This used to be in HTML format, but it
        is no longer, but function name has not been updated.

        the log is in json format string, with lines like this, list of dicts,
            [ { "item": item, "log": log, "rowcolor": color, "fs": fs}, ... ]

        :param summary: a string json, list of dicts
        """
        self._record["html_summary"] = summary

    def record_publish(self, type="result"):
        ruid = str(uuid.uuid4())
        _file = type + "_" + ruid + ".json"
        self._record["meta"]["ruid"] = ruid

        # NOTE: this new 'd' becomes the record saved in the result json file!
        d = {"result": self._record,
             "file": _file,
             "processor": self._record["meta"]["processor"],
             "from": "{}.record_publish".format(__class__.__name__)}

        if "from" in d: d.pop("from")  # remove debugging key
        if "type" in d: d.pop("type")  # remove event key

        with open(_file, 'w') as fp:
            json.dump(d, fp, indent=2)
        self.logger.info("Created: {}".format(_file))

        return _file

    def __repr__(self): return str(self._record)
