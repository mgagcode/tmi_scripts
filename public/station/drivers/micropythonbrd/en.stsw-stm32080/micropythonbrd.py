#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Martin Guthrie, copyright, all rights reserved, 2018

"""


class MicroPythonBrd(object):
    """ MicroPython Board driver
        see http://docs.micropython.org/en/latest/pyboard/
            http://docs.micropython.org/en/latest/pyboard/pyboard/quickref.html

        - when board is plugged in, it shows up as a flash drive
        - you and edit main.py to make a stand alone program
            - this is ot what we want, we want to write code here, and
              have the action take place on the board... how to do that?
            - you can connect to the board via a serial port
            - once there, we are in a python shell, can send commands directly

            - maybe this https://github.com/dhylands/json-ipc
            - https://github.com/dhylands/rshell


    """

    def __init__(self, port):
        self.port = port
        # TODO: some line of test

    def led(self, num, enable=True):
        pass



if __name__ == "__main__":

    port = "COM1" # or some other COM, see device manager on windows to figure out

    brd = MicroPythonBrd(port)


# https://forum.micropython.org/viewtopic.php?f=6&t=4965&sid=4222863b6ed4aef98386089d7c048e23

# https://forum.micropython.org/viewtopic.php?f=6&t=5071&sid=4222863b6ed4aef98386089d7c048e23

# here is example found at https://forum.micropython.org/viewtopic.php?f=6&t=1020&hilit=pc+control&start=10
# It opens a serial connection to the pyboard and runs a command...
"""
# need to reference the win32 serial stuff
import serial
import time
import binascii

# mocks the bbio interface
# and talks to the attached pyb board using its repl

class I2CDev:
    pass

    def __init__(self, bus):
        # open the serial port
        self.serial = serial.Serial("COM3", 115200, timeout=1)
        pass

    def enter_repl(self):
        self.serial.write(b'\r\x02\x04')  # soft reset
        time.sleep(0.25)  # small delay
        self.serial.flushInput()
        #data = self.serial.read

        # send ^A to go into raw repl
        # leaving the '>' in the input buffer
        self.serial.write(b'\x01')
        data = self.serial.readline();
        data = self.serial.readline();
        pass

    def read_packet(self): # , until):
        packet = self.serial.read(1)
        while not packet.endswith(b'\x04'):
            packet += self.serial.read(1)
        return packet[:-1]

    def send_command(self, cmd):
        print(cmd)
        #check weve got a prompt
        data = self.serial.read(1)
        if data != b'>':
            #pass
            raise IOError
        # send out the data
        self.serial.write(bytes(cmd, encoding='utf8'))
        # send eof
        self.serial.write(b'\x04')
        # check OK
        data = self.serial.read(2)
        if data != b'OK':
            raise IOError
        # pick up answers
        reply = self.read_packet()
        error = self.read_packet()
        print(reply)
        return reply, error

    def eval_command(self, cmd):
        return self.send_command("print({})".format(cmd))

    def open(self):
        self.enter_repl()
        # and establish an i2c object to chat with
        self.send_command("from pyb import I2C")
        self.send_command("import ubinascii")
        self.send_command("i2c=I2C(1,I2C.MASTER)")

    def write(self, address, data):
        # formay python statement to run on the pyb
        s = "i2c.send(bytes({0}),{1})".format(data, address).replace(' ','')
        self.send_command( s ) #"i2c.send(bytes({0}),{1})".format(data, address))

    def readTransaction(self, address, reg, count):
        try:
            data, error = self.eval_command("ubinascii.hexlify(i2c.mem_read({0},{1},{2}))".format(count, address, reg))
            # b'00[nnnnnnnnnnn]'\r\n
            # nb occasionally we get back empty in repl and raw repl modes
            r = data[2:-3]
            # ================================================
            if len(r) != 2 * count:
                print("WTF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                # did we get an error
                self.open()
                data, error = self.eval_command("ubinascii.hexlify(i2c.mem_read({0},{1},{2}))".format(count, address, reg))
                r = data[2:-3]
            # ================================================

            wtf = binascii.unhexlify(r)
            return list(wtf) ##[0]
        except:
            # reallocate or nothing works??
            self.open()
            #raise IOError

"""
