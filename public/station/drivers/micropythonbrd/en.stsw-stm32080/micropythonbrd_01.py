#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import drivers.micropythonbrd.pyboard as pyboard
import time
import sys

LED_DELAY_S = 0.1


def execbuffer(buf):
    try:
        ret, ret_err = pyb.exec_raw(buf, timeout=None, data_consumer=None)
    except pyboard.PyboardError as er:
        print(er)
        pyb.close()
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    if ret_err:
        pyb.exit_raw_repl()
        pyb.close()
        pyboard.stdout_write_bytes(ret_err)
        sys.exit(1)

    if ret: print(ret.decode("utf-8").strip())


pyb = pyboard.Pyboard('COM3')

pyb.enter_raw_repl()  # this does a softreset....!

while True:

    try:
        execbuffer('pyb.LED(1).on()')
        time.sleep(LED_DELAY_S)
        pyb.exec_raw('pyb.LED(1).off()')
        time.sleep(LED_DELAY_S)
        execbuffer('pyb.LED(1).on()')
        time.sleep(LED_DELAY_S)
        execbuffer('pyb.LED(1).off()')
        time.sleep(LED_DELAY_S)
        execbuffer('pyb.LED(1).on()')
        time.sleep(LED_DELAY_S)
        execbuffer('pyb.LED(1).off()')

        execbuffer('sw = pyb.Switch()')
        execbuffer('print(sw.value())')

    except KeyboardInterrupt:
        break

pyb.exit_raw_repl()
pyb.close()
print("----")
