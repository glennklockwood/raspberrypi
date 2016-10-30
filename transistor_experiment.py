#!/usr/bin/env python
"""
Demonstrate using the MCP3008 and MCP41010 classes together to change the
voltage feeding into the base of a NPN transistor and observe the resulting
effects on the collector and emitter leads.

This is a more elaborate implementation of simple_transistor_exp.py which
should be included in this repository.
"""

import spi.mcp3008 as mcp3008
import spi.mcp41010 as mcp41010
import time

_VDD = 3.3

if __name__ == '__main__':
    adc = mcp3008.MCP3008(clk=18, cs=25, mosi=24, miso=23, verbose=False)
    digipot = mcp41010.MCP41010(clk=19, cs=13, mosi=26, miso=None, verbose=False)

    for resist_val in range(1 << 8):
        digipot.set_value(resist_val)
        sum_values = [ 0.0 ] * 3  # measuring 3 channels
        num_values = [ 0.0 ] * 3
        time.sleep(0.1)
        for _ in range(10): # take ten measurements for each resistance
            for i in range(len(sum_values)):
                sum_values[i] += _VDD * adc.measure(i) / 1023.0 
                num_values[i] += 1
            time.sleep(0.1)
        print "%4.2f %4.2f %4.2f %5d" % (sum_values[0] / num_values[0],
                                         sum_values[1] / num_values[1],
                                         sum_values[2] / num_values[2],
                                         10000 * resist_val / ((1 << 8) - 1))
