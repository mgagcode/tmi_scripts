import os
import sys
import argparse
import json
import logging
import logging.handlers as handlers


logger = None
SCRIPT_PATH = "public/station/scripts/TMIDemoRecordV1/prod_v0/prod_0.tmiscr"


def setup_logging(log_file_name_prefix="log", level=logging.INFO, path="./log"):
    global logger
    logger = logging.getLogger("TMI")
    logger.setLevel(level)

    log_file_name_prefix = os.path.basename(log_file_name_prefix)

    if not os.path.exists(path): os.makedirs(path)

    # Here we define our formatter
    FORMAT = "%(asctime)s %(threadName)15s %(filename)25s:%(lineno)4s - %(name)30s:%(funcName)20s() %(levelname)-5.5s : %(message)s"
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

    success, script = read_json_file_to_dict(args["script"])
    if not success:
        logger.error(script)
        return 1

    # validate script
    if not script_validated(script):
        logger.error("Script failed to validate")
        return 1



    return 0


if __name__ == "__main__":
    retcode = main()
    sys.exit(retcode)