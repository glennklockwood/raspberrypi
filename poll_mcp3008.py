#!/usr/bin/env python
"""
Demonstrate how to use the MCP3008 class
"""

import mcp3008
import time

dev = mcp3008.MCP3008(clk=18, cs=25, mosi=24, miso=23, verbose=False)

print "%8s Ch#0 Ch#1 Ch#2 Ch#3 Ch#4 Ch#5 Ch#6 Ch#7" % "Time"
while True:
    measurements = time.strftime("%H:%M:%S")
    for channel in range(8):
        measurements += " %4d" % dev.measure(channel)
    print measurements
    time.sleep(5.0)

