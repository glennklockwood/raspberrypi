#!/usr/bin/env python
#
#  poll_thermistor.py - demonstrate how to collect measurements from a
#    thermistor attached to an analog-to-digital converter.
#
#  Glenn K. Lockwood, October 2016
#
"""
Poll a thermistor attached through an MCP3008 ADC and print the reading to
stdout.
"""

import os
import sys
import time
import mcp3008spi
from RPi import GPIO

_SENSOR_CHANNEL = 0
_SECONDS_PER_SAMPLE = 5.0
_SERIES_RESISTOR_OHMS = 10000.0

def get_temperature(resistance, table):
    """
    Interpolate temperature from temperature table
    """
    for i, r_t in enumerate(table):
        if r_t[0] > resistance:
            if i > 0:
                slope = float(r_t[1] - table[i-1][1])
                slope /= float(r_t[0] - table[i-1][0])
                return (resistance - table[i-1][0]) * slope + table[i-1][1]
            else:
                return r_t[1]
        else:
            continue
    raise Exception("R = %.2f out of bounds" % resistance)

def load_temperatures(filename):
    """
    Load temperature table as tuples of (resistance, temperature) from a
    space-separated text file.  This file should contain one pair of values
    per line, where a pair of values is:

        temperature(C) resistance(kohm)

    this table can be generated from the data available at

        https://cdn-shop.adafruit.com/datasheets/103_3950_lookuptable.pdf

    which corresponds to a 10 KOhm thermistor.
    """
    ### load temperature table
    temperatures = []
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            for line in fp:
                line = line.strip()
                if line.startswith('#'):
                    continue
                t_c, r_kohm = line.split()
                t_c = int(t_c)
                r_kohm = float(r_kohm) * 1000.0 # convert from kohm to ohm
                temperatures.append((r_kohm, t_c))
        ### sort because get_temperature assumes it
        temperatures = sorted(temperatures, key=lambda x: x[0])
    print "Loaded %d values from temperature table" % len(temperatures)
    return temperatures

def poll_temperature():
    """
    Run a loop that polls the ADC and converts the return value to a
    temperature
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "temperatures.txt"
    temperatures = load_temperatures(filename)

    avg_reading = 0.0
    elapsed_secs = 0.0
    count = 0
    print "%-19s %9s %9s %9s %9s" % ("Date", "Raw read", "Ohms", "Volts",
                                     "Temp(C)")
    while True:
        raw_reading = mcp3008spi.mcp3008_get(_SENSOR_CHANNEL)
        avg_reading += raw_reading
        elapsed_secs += 1.0
        count += 1

        ### average over many samples
        if elapsed_secs >= _SECONDS_PER_SAMPLE:
            avg_reading /= float(count)
            resistance = _SERIES_RESISTOR_OHMS / (1023.0 / avg_reading - 1.0)
            voltage = 3.3 * avg_reading / 1023.0
            temperature = get_temperature(resistance, temperatures)

            print "%-19s %9d %9d %9.2f %9.1f" % (
                time.strftime("%Y-%m-%d %H:%M:%S"),
                int(avg_reading),
                int(resistance),
                voltage,
                temperature)
            elapsed_secs = 0.0
            avg_reading = 0.0
            count = 0

        time.sleep(1.0)

if __name__ == '__main__':
    try:
        poll_temperature()
    except:
        GPIO.cleanup()
        raise
