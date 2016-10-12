#!/usr/bin/env python
"""
A very simple SPI implementation that allows you to assign arbitrary GPIO pins
to act as SPI wires and put/get data.

Implemented as a class so that the pin mappings don't need to be passed around
as a bunch of input arguments to put/get as in the mcp3008spi.py script; you
just create an SPI object and pass it around or create a subclass specific to
the SPI endpoint's protocol.
"""

import sys
from RPi import GPIO

class SPI(object):
    def __init__(self, clk, cs, mosi, miso, verbose=False):
        """Create a simple SPI pin map and configure an initial known state"""
        self.clk = clk
        self.cs = cs
        self.mosi = mosi
        self.miso = miso
        if verbose:
            self.verbose = True
        else:
            self.verbose = False
        GPIO.setmode(GPIO.BCM)
        ### sometimes you don't need an input or an output, so they're optional
        if self.mosi:
            GPIO.setup(self.mosi, GPIO.OUT, initial=GPIO.LOW)
        if self.miso:
            GPIO.setup(self.miso, GPIO.IN)
        GPIO.setup(self.clk, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.cs, GPIO.OUT, initial=GPIO.HIGH)

    def __del__(self):
        GPIO.cleanup()

    def put(self, data, bits):
        """send a bit vector of a given length over MOSI"""
        data_buf = data
        packet = ""
        GPIO.output(self.cs, GPIO.LOW)
        try:
            for _ in range(bits):
                if data_buf & (2**(bits-1)):
                    GPIO.output(self.mosi, GPIO.HIGH)
                    packet += "1"
                else:
                    GPIO.output(self.mosi, GPIO.LOW)
                    packet += "0"
                data_buf <<= 1
                GPIO.output(self.clk, GPIO.HIGH)
                GPIO.output(self.clk, GPIO.LOW)
            self._vprint("Sent [%s]" % packet)
        except:
            GPIO.output(self.cs, GPIO.HIGH)
            raise

        GPIO.output(self.cs, GPIO.HIGH)

    def get(bits):
        """get a bit vector of a given length via MISO"""
        data_buf = 0x0

        packet = ""
        GPIO.output(self.cs, GPIO.LOW)
        try:
            for _ in range(bits):
                GPIO.output(self.clk, GPIO.HIGH)
                GPIO.output(self.clk, GPIO.LOW)
                data_buf <<= 1
                if GPIO.input(self.miso):
                    data_buf |= 0x1
                    packet += "1"
                else:
                    packet += "0"
            self._vprint("Recv [%s]" % packet)
        except:
            GPIO.output(self.cs, GPIO.HIGH)
            raise

        GPIO.output(self.cs, GPIO.HIGH)
        return data_buf

    def _vprint(self, msg):
        """print messages only when debugging is enabled"""
        if self.verbose:
            sys.stderr.write(msg + "\n")
