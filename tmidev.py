import os
import sys
import argparse
import json
import logging
import logging.handlers as handlers
import importlib

from public.station.api import ResultAPI
from core.tmi_core_helpers import SharedState

logger = None
SCRIPT_PATH = "public/station/scripts/TMIDemoRecordV1/prod_v0/prod_0.tmiscr"


class attrdict(dict):
    """
    Attribute Dictionary.

    Enables getting/setting/deleting dictionary keys via attributes.
    Getting/deleting a non-existent key via attribute raises `AttributeError`.
    Objects are passed to `__convert` before `dict.__setitem__` is called.

    This class rebinds `__setattr__` to call `dict.__setitem__`. Attributes
    will not be set on the object, but will be added as keys to the dictionary.
    This prevents overwriting access to built-in attributes. Since we defined
    `__getattr__` but left `__getattribute__` alone, built-in attributes will
    be returned before `__getattr__` is called. Be careful::

        >>> a = attrdict()
        >>> a['key'] = 'value'
        >>> a.key
        'value'
        >>> a['keys'] = 'oops'
        >>> a.keys
        <built-in method keys of attrdict object at 0xabcdef123456>

    Use `'key' in a`, not `hasattr(a, 'key')`, as a consequence of the above.
    """
    def __init__(self, *args, **kwargs):
        # We trust the dict to init itself better than we can.
        dict.__init__(self, *args, **kwargs)
        # Because of that, we do duplicate work, but it's worth it.
        for k, v in self.items():
            self.__setitem__(k, v)

    def __getattr__(self, k):
        try:
            return dict.__getitem__(self, k)
        except KeyError:
            # Maintain consistent syntactical behaviour.
            raise AttributeError(
                "'attrdict' object has no attribute '" + str(k) + "'"
            )

    def __setitem__(self, k, v):
        dict.__setitem__(self, k, attrdict.__convert(v))

    __setattr__ = __setitem__

    def __delattr__(self, k):
        try:
            dict.__delitem__(self, k)
        except KeyError:
            raise AttributeError(
                "'attrdict' object has no attribute '" + str(k) + "'"
            )

    @staticmethod
    def __convert(o):
        """
        Recursively convert `dict` objects in `dict`, `list`, `set`, and
        `tuple` objects to `attrdict` objects.
        """
        if isinstance(o, dict):
            o = attrdict(o)
        elif isinstance(o, list):
            o = list(attrdict.__convert(v) for v in o)
        elif isinstance(o, set):
            o = set(attrdict.__convert(v) for v in o)
        elif isinstance(o, tuple):
            o = tuple(attrdict.__convert(v) for v in o)
        return o


class TMIChanCon(object):

    def __init__(self, num=0, script=None, shared_state=None, script_filename="UNKNOWN", operator="UNKNOWN"):
        self.logger = logging.getLogger("TMI.{}.{}".format(__class__.__name__, num))
        self.ch = num
        self.script = script
        self.shared_state = shared_state
        self.operator = operator

        record_handler = script["config"]["record_handler"]
        i = importlib.import_module(record_handler)
        klass = record_handler.split(".")[-1]
        record_handler_klass = getattr(i, klass)

        self.record = record_handler_klass(0, "tmidev", script_filename)
        self.record.record_info_set(script.get("info", {}))
        self.record.record_record_meta_init()

    def item_start(self):
        d = {"item": self._item,             # item dict from the script, ex {"id": "TST000", "enable": true,  "args": {"min": 0, "max": 2}}
             "options": self._options,       # options dict from the script, ex { "fail_fast": false }
             "record": self.record,

             # TODO: add more stuff as needed
            }
        self.record.record_item_create(d["item"]["id"])
        return attrdict(d)

    def item_end(self, item_result_state=ResultAPI.RECORD_RESULT_PASS, _next=None):
        self.logger.debug("{}, {}".format(self._item["id"], item_result_state))

        if self.record.record_test_get_result() not in [ResultAPI.RECORD_RESULT_UNKNOWN]:
            # there must have been another early failure, either a timeout or crash...
            # bail on processing, assume its already been done...
            self.logger.warning("record_test_set_result already set... aborting")
            return

        # process a list of results, set the final state to the first non pass state
        if isinstance(item_result_state, list):
            _final = ResultAPI.RECORD_RESULT_PASS
            for result in item_result_state:
                if result is not ResultAPI.RECORD_RESULT_PASS:
                    _final = result
                    break
            item_result_state = _final

        self.record.record_test_set_result(item_result_state)
        self.record.record_item_end()

    def log_bullet(self, text, ovrwrite_last_line):
        self.logger.info("BULLET: {}".format(text))

    def run(self):

        for test in self.script["tests"]:

            self._options = test["options"]

            logger.info("Module: {}".format(test["module"]))
            test_module = importlib.import_module(test["module"])
            klass = test["module"].split(".")[-1]
            logger.debug("class: {}".format(klass))

            test_module_klass = getattr(test_module, klass)
            test_klass = test_module_klass(controller=self, ch_num=self.ch, shared_state=self.shared_state)

            for item in test["items"]:
                logger.info("ITEM: {}".format(item))
                if item.get("enable", True):
                    self._item = item
                    func = getattr(test_klass, item["id"])
                    func()

        self.record.record_record_meta_fini()
        self.record.record_publish()


def setup_logging(log_file_name_prefix="log", level=logging.INFO, path="./log"):
    global logger
    logger = logging.getLogger("TMI")
    logger.setLevel(level)

    log_file_name_prefix = os.path.basename(log_file_name_prefix)

    if not os.path.exists(path): os.makedirs(path)

    # Here we define our formatter
    FORMAT = "%(relativeCreated)5d %(filename)20s:%(lineno)4s - %(name)21s:%(funcName)16s() %(levelname)-5.5s : %(message)s"
    formatter = logging.Formatter(FORMAT)

    allLogHandler_filename = os.path.join(path, "".join([log_file_name_prefix, ".log"]))
    allLogHandler = handlers.RotatingFileHandler(allLogHandler_filename, maxBytes=1024 * 1024, backupCount=4)
    allLogHandler.setLevel(logging.INFO)
    allLogHandler.setFormatter(formatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    logger.addHandler(allLogHandler)
    logger.addHandler(consoleHandler)


def read_json_file_to_dict(file):
    if os.path.isfile(file):
        content = []
        with open(file) as json_data:
            for line in json_data:
                if line.strip().startswith('#'):
                    content.append("\n")
                else:
                    content.append(line)

        try:
            _dict = json.loads("".join(content))

        except Exception as e:
            logger.error(e)
            return False, e

    else:
        msg = "Unable to find json file %s" % file
        logger.error(msg)
        return False, msg
    return True, _dict


def parse_args():
    """
    :return: args
    """
    epilog = """
    Usage examples:
    TBD
    """
    parser = argparse.ArgumentParser(description='TMIDev',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)

    parser.add_argument("--script",
                        dest="script",
                        action="store",
                        default=SCRIPT_PATH,
                        help="Path to script files")

    args = parser.parse_args()
    args_dict = vars(args)
    return args_dict


def script_validated(script):
    if not script.get("config", False):
        logger.error("Script is missing 'config' section")
        return False

    if not script["config"].get("record_handler", False):
        logger.error("Script is missing 'config.record_handler' section")
        return False

    if not script["config"].get("channel_hw_driver", False):
        logger.error("Script is missing 'config.channel_hw_driver' section")
        return False

    # TODO: add more stuff, check imports....

    logger.info("Script passed validation tests")
    return True


def main():
    setup_logging(log_file_name_prefix="tmidev", path="log")

    args = parse_args()
    logger.info("args: {}".format(args))
    if args is None:
        logger.error("Failed to parse args")
        return 1

    # read script
    success, script = read_json_file_to_dict(args["script"])
    if not success:
        logger.error(script)
        return 1

    # validate script
    if not script_validated(script):
        logger.error("Script failed to validate")
        return 1

    shared_state = SharedState()

    con = TMIChanCon(0, script, shared_state, args["script"])

    con.run()

    return 0


if __name__ == "__main__":
    retcode = main()
    sys.exit(retcode)