#!/usr/bin/env python
"""
Set a resistance on MCP41010 (digital potentiometer), then measure the effect
using MCP3008 (analog-digital converter).
"""

import spi
import time

### use two independent SPI buses, but daisy chaining then is also valid
adc = spi.SPI(clk=18, cs=25, mosi=24, miso=23, verbose=False)
digipot = spi.SPI(clk=19, cs=13, mosi=26, miso=None, verbose=False)

### iterate over all possible resistance values (8 bits = 256 values)
for resist_val in range(256):
    ### set the resistance on the MCP41010 #############################
    cmd = int("00010001", 2)
    # make room for resist_val's 8 bits
    cmd <<= 8
    digipot.put(cmd|resist_val, bits=16)

    ### wait to allow voltage transients to subside
    time.sleep(0.2)

    ### get the voltage from the MCP3008 ###############################
    voltages = [0, 0, 0]
    for channel in range(len(voltages)):
        # set the start bit, single-ended mode bit, and 3 channel select bits
        cmd = int("11000", 2) | channel
        # read 1 null bit, then 10 data bits
        cmd <<= 10 + 1
        value = adc.put_get(cmd, bits=16)
        # mask off everything but the last 10 read bits
        value &= 2**10 - 1
        voltages[channel] = 3.3 * value / 1023.0

    print "%4.2f %4.2f %4.2f %5d" % (voltages[0], voltages[1], voltages[2],
                                     10000.0 * resist_val / 255.0)
