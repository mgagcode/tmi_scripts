#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import drivers.micropythonbrd.pyboard as pyboard
import glob
import sys
import serial
import time
import logging
import json
import argparse


def serial_ports():
    # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class TMIMicroPyBrd(object):
    """


    LESSONS:
    1) pyb.enter_raw_repl()  # this does a softreset....!
    2) sometimes functions won't return a value, for example, pyb.freq(),
       need to wrap in a print, print(pyb.freq())
    3) References,
       http://docs.micropython.org/en/v1.9.3/pyboard/pyboard/quickref.html
       http://docs.micropython.org/en/v1.9.3/esp8266/esp8266/tutorial/filesystem.html
    """

    class StubLogger(object):
        """ stubb out logger if none is provided"""
        # TODO: support print to console.
        def info(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
        def debug(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass
        def critical(self, *args, **kwargs): pass


    logger = StubLogger()
    BAUDRATE = 115200

    def __init__(self, logger=None):
        if logger: self.logger = logger
        self.pyb = None
        self.channel = None
        self.logger.info("Done")
        self.serial = None

    def _enter_raw_repl(self):
        # A port/hack of pyboard to test a port for micropython
        self.serial.write(b'\r\x03\x03') # ctrl-C twice: interrupt any running program
        # flush input (without relying on serial.flushInput())
        n = self.serial.inWaiting()
        while n > 0:
            self.serial.read(n)
            n = self.serial.inWaiting()
        self.serial.write(b'\r\x01') # ctrl-A: enter raw REPL
        data = self.serial.read(50)
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
            self.logger(data)
            return False
        return True

    def scan_ports(self):
        """ Finds the port for the channel
        :return:
        """
        ports = []
        port_candidates = serial_ports()
        self.logger.info("Looking for Pyboard in {}".format(port_candidates))
        for port in port_candidates:
            success = False
            try:
                self.serial = serial.Serial(port, baudrate=self.BAUDRATE, timeout=1, interCharTimeout=1)
                success = self._enter_raw_repl()

            except Exception as e:
                self.logger.debug(e)
                self.logger.info("NO micropython on {}".format(port))

            finally:
                self.serial.close()

            if success:
                self.logger.info("Found micropython on {}".format(port))
                # now open proper way and get stored channel configuration...
                self.open(port)

                self.execbuffer('pyb.LED(1).on()')
                time.sleep(0.5)
                self.execbuffer('pyb.LED(1).off()')
                time.sleep(0.5)

                channel = self.get_channel()

                self.pyb.close()
                ports.append((port, channel))
            else:
                self.logger.info("NO micropython on {}".format(port))

        self.logger.info("Found {}".format(ports))
        return ports

    def open(self, port):
        self.pyb = pyboard.Pyboard(port)
        self.pyb.enter_raw_repl()  # this does a softreset on micropython

    def close(self):
        if self.pyb: self.pyb.close()

    def execbuffer(self, buf):
        # this was copied from pyboard.py
        try:
            ret, ret_err = self.pyb.exec_raw(buf + '\n', timeout=1, data_consumer=None)
        except pyboard.PyboardError as er:
            print(er)
            self.pyb.close()
            return False, None
        except KeyboardInterrupt:
            return False, None
        if ret_err:
            self.pyb.exit_raw_repl()
            self.pyb.close()
            pyboard.stdout_write_bytes(ret_err)
            return False, None

        if ret:
            return True, ret.decode("utf-8").strip()
        return True, ""

    def get_channel(self):
        cmds = ['import os', 'print(os.listdir())']
        cmd = "\n".join(cmds)
        success, result = self.execbuffer(cmd)
        if success:
            self.logger.debug("{} {}".format(success, result))
            # string result => ['main.py', 'pybcdc.inf', 'README.txt', 'CH1', 'boot.py']
            files = json.loads(result.replace("'", '"'))
            for f in files:
                if f.startswith("CH"):
                    channel = int(f[2:])
                    return channel
        return None

    def set_channel(self, channel):
        pass


def parse_args():
    epilog = """
    Usage examples:
    """
    parser = argparse.ArgumentParser(description='tmi_microython',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)

    parser.add_argument("-v", '--verbose', dest='verbose', default=0, action='count', help='Increase verbosity')
    parser.add_argument("--version", dest="show_version", action='store_true', help='Show version and exit')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(lineno)4s %(message)s')

    pyb = TMIMicroPyBrd(logging)
    pyb.scan_ports()
    pyb.close()
