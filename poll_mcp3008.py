#!/usr/bin/env python
"""
Demonstrate how to use the MCP3008 class
"""

import spi.mcp3008 as mcp3008
import argparse
import time


def poll_mcp(delay=5.0, voltage=None, resistances=None):
    """
    Periodically poll MCP3008 device and report values for each channel.  If
    reference voltage is supplied, report the measured voltage; if reference
    voltage and series resistance is reported, report measured resistance.
    """
    if resistances is not None and len(resistances) != 8:
        raise Exception("Resistances must be specified for each channel")

    dev = mcp3008.MCP3008(clk=18, cs=25, mosi=24, miso=23, verbose=False)

    print "%8s Ch#0 Ch#1 Ch#2 Ch#3 Ch#4 Ch#5 Ch#6 Ch#7" % "Time"
    while True:
        measurements = time.strftime("%H:%M:%S")

        ### if we know the reference voltage, we can report voltage drop
        if voltage is not None and resistances is None:
            for channel in range(8):
                measurements += " %4.2f" % ( voltage * dev.measure(channel) / 1023.0 )

        ### if we know reference voltage and series resistances, we can
        ### calculate resistance corresponding to voltage drop
        elif voltage is not None and resistances is not None:
            for channel in range(8):
                reading = dev.measure(channel)
                if reading == 0:
                    value = 0
                else:
                    value = (resistances[channel] / (1023.0 / reading - 1.0))
                measurements += " %4d" % value 

        ### no input voltage means we can only report raw measurements
        else:
            for channel in range(8):
                measurements += " %4d" % dev.measure(channel)

        print measurements
        time.sleep(delay)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--voltage', '-v', type=float, help="reference voltage")
    parser.add_argument('--resistance', '-r', type=str, help="comma-separated list of series resistances (ohms)")
    parser.add_argument('--delay', '-d', type=float, default=5.0, help="delay between measurements (Seconds)")
    args = parser.parse_args()

    ### --resistance can be a single value (same resistance for all channels)
    ### or a comma-separated list of eight resistances (one for each channel)
    resistances=None
    if args.resistance is not None:
        resistances = [ int(x) for x in args.resistance.split(',') ]
        if len(resistances) == 1:
            resistances = [ resistances[0] ] * 8

    poll_mcp(delay=args.delay, voltage=args.voltage, resistances=resistances)
