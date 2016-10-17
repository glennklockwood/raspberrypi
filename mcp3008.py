#!/usr/bin/env python
"""
mcp3008.py - provide a class for interacting with MCP3008 ADC chips
"""

import sys
import RPi.GPIO as GPIO
import spi

class MCP3008(spi.SPI):
    def __init__(self, clk, cs, mosi, miso, verbose=False):
        spi.SPI.__init__(self, clk, cs, mosi, miso, verbose)

    def __del__(self):
        spi.SPI.__del__(self)
        
    def measure(self, channel):
        """Get a single 10-bit measurement from a single channel of MCP3008
        The MCP3008 protocol is described as:

        1. The first clock received with CS low and DIN high will constitute a
           start bit.
        2. The SGL/DIFF bit follows the start bit and will determine if the
           conversion will be done using single-ended or differential input mode
        3. The next three bits (D0, D1 and D2) are used to select the input channel
           configuration.
        4. The device will begin to sample the analog input on the fourth rising
           edge of the clock after the start bit has been received.
        5. The sample period will end on the falling edge of the fifth clock
           following the start bit.
        6. Once the D0 bit is input, one more clock is required to complete the
           sample and hold period (DIN is a "don't care" for this clock).
        7. On the falling edge of the next clock, the device will output a low null
           bit.
        8. The next 10 clocks will output the result of the conversion with MSB
           first
        """

        if channel < 0 or channel > 7:
            raise Exception("channel out of range")

        cmd = int("11000", 2) | channel

        ### get 1 NULL bit + 10 data bits in MSR order
        read_bits = 10 + 1

        ### the length of cmd determines length of read too, so shift it out
        cmd <<= read_bits

        ### send and receive data
        buf = self.put_get(cmd, bits=(read_bits + 5))

        ### mask off the command and NULL bits
        buf &= 2**(read_bits-1)-1

        return buf 
