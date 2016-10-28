#!/usr/bin/env python
"""
mcp41010.py - provide a class for interacting with MCP41010 digital
potentiometer chips
"""
import spi
from RPi import GPIO

class MCP41010(spi.SPI):
    def __init__(self, clk, cs, mosi, miso, verbose=False):
        spi.SPI.__init__(self, clk, cs, mosi, miso, verbose)

    def __del__(self):
        spi.SPI.__del__(self)

    def set_value(self, value):
        """
        Send a 16-bit command to the MCP41010.  The eight most significant bits
        comprise the command, and the eight least significant bits are the value
        to be set.

        The 8-bit command are comprised of 4 bits of command selection and 4
        bits of potentiometer selections.

        Command selection: XX00 and XX11 - no-op
                           XX01 - modify potentiometer
                           XX10 - enable shutdown mode
        For MCP41010 (single-channel), the potentiometer selection is always
        XXX1.  X represents a "don't care" bit.
        """
        if value >= (1 << 8) or value < 0:
            raise Exception("Invalid value")

        cmd = int("00010001",2) << 8
        self.put(cmd|value, 16)

    def set_shutdown(self):
        """
        Set shutdown mode bit
        """
        cmd = 1 << 13
        self.put(cmd, 16)
