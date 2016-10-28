#!/usr/bin/env python
"""
Use both the MCP3008 analog-digital converter along with the MCP41010 digital
potentiometer to set a resistance, then masure it.
"""

import spi.mcp3008 as mcp3008
import spi.mcp41010 as mcp41010
import time

_VDD = 3.3

if __name__ == '__main__':
    adc = mcp3008.MCP3008(clk=18, cs=25, mosi=24, miso=23, verbose=False)
    digipot = mcp41010.MCP41010(clk=19, cs=13, mosi=26, miso=None, verbose=False)

    for resist_val in range(1, 1 << 8, 2):
        digipot.set_value(resist_val)
        time.sleep(0.1)
        voltage = _VDD * adc.measure(7) / 1023.0 
        print "%4.2f %5d" % (voltage, 10000 * resist_val / ((1 << 8) - 1))
