#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""
import drivers.micropythonbrd.pyboard as pyboard
import time
import sys

LED_DELAY_S = 0.01

# LESSONS:
# 1) pyb.enter_raw_repl()  # this does a softreset....!
# 2) sometimes functions won't return a value, for example, pyb.freq(),
#    need to wrap in a print, print(pyb.freq())
# 3) References,
#    http://docs.micropython.org/en/v1.9.3/pyboard/pyboard/quickref.html
#    http://docs.micropython.org/en/v1.9.3/esp8266/esp8266/tutorial/filesystem.html


# this was copied from pyboard.py
def execbuffer(buf):
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
#execbuffer('pyb.freq()')         # this doesn't work.... :(
execbuffer('print(pyb.freq())')  # BUT this does!

execbuffer('rtc = pyb.RTC()')
execbuffer('print(rtc.datetime())')

execbuffer('def myFunc():\n print("myfunc")\n')
execbuffer('\n')
execbuffer('\n')
execbuffer('\n')

execbuffer('myFunc()')

execbuffer('sw = pyb.Switch()')
execbuffer("adc = pyb.ADC(pyb.Pin('X19'))")

while True:

    try:
        execbuffer('pyb.LED(1).on()')
        time.sleep(LED_DELAY_S)
        execbuffer('pyb.LED(1).off()')
        time.sleep(LED_DELAY_S)

        execbuffer('print(sw.value())')
        execbuffer('print(adc.read())')

    except KeyboardInterrupt:
        break

pyb.exit_raw_repl()
pyb.close()
print("----")
