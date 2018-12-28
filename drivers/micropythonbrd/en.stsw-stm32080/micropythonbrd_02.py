#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import drivers.micropythonbrd.pyboard as pyboard
import time
import sys

LED_DELAY_S = 0.1

# this was copied from pyboard.py
def execbuffer(buf):
    #print(buf)
    try:
        ret, ret_err = pyb.exec_raw(buf + '\n', timeout=1, data_consumer=None)
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

execbuffer('import pyb')
execbuffer('pyb.freq()')  # this doesn't work.... :(

execbuffer('rtc = pyb.RTC()')
execbuffer('print(rtc.datetime())')

execbuffer('def myFunc():\n print("myfunc")\n')
execbuffer('\n')
execbuffer('\n')
execbuffer('\n')

execbuffer('print(pyb.freq())')
execbuffer('myFunc()')

while True:

    try:
        execbuffer('pyb.LED(1).on()')
        time.sleep(LED_DELAY_S)
        pyb.exec_raw('pyb.LED(1).off()')
        time.sleep(LED_DELAY_S)

        execbuffer('sw = pyb.Switch()')
        execbuffer('print(sw.value())')

    except KeyboardInterrupt:
        break

pyb.exit_raw_repl()
pyb.close()
print("----")
