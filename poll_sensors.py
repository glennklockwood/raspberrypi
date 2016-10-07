#!/usr/bin/env python
#
#  poll_channels.py - demonstrate how to collect measurements from analog
#    components attached to an eight-channel analog-to-digital converter.
#
#  Glenn K. Lockwood, October 2016
#
"""
Poll channels of an MCP3008 ADC and print the readings to stdout.
"""

import os
import sys
import time
import subprocess
import mcp3008spi
import poll_thermistor
from RPi import GPIO

SECONDS_PER_SAMPLE = 60.0

### Number of channels on ADC chip
NUM_CHANNELS = 8

### Define some logical meaning to each channel
CHANNEL_THERM = 0
CHANNEL_PHOTO = 1

### Resistance of resistor attached to each channel in series
SERIES_RESISTOR_OHMS = [ 10000.0 ] * NUM_CHANNELS

def poll_channels():
    """
    Run a loop that polls the ADC and converts the return value (if applicable)
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "temperatures.txt"
    temperatures = poll_thermistor.load_temperatures(filename)

    ### initialize 8 channels of readings
    avg_reading = [ 0.0 ] * NUM_CHANNELS
    elapsed_secs = 0.0
    count = 0
    print "%-19s %6s %6s %6s %9s %6s %6s %6s" % ("Date",
                               "ThRaw", "ThOhms", "ThVolt", "Temp(C)",
                               "PhRaw", "PhOhms", "PhVolt")

    while True:
        avg_reading[CHANNEL_THERM] += mcp3008spi.mcp3008_get(CHANNEL_THERM)
        avg_reading[CHANNEL_PHOTO] += mcp3008spi.mcp3008_get(CHANNEL_PHOTO)

        elapsed_secs += 1.0
        count += 1

        ### average over many samples
        if elapsed_secs >= SECONDS_PER_SAMPLE:
            avg_reading = [ x / float(count) for x in avg_reading ]
            voltage = [ 3.3 * x / 1023.0 for x in avg_reading ]
            resistance = [ 0.0 ] * NUM_CHANNELS
            for i, x in enumerate(avg_reading):
                if x > 0:
                    resistance[i] = SERIES_RESISTOR_OHMS[i] / (1023.0 / x - 1.0)
            temperature = poll_thermistor.get_temperature(resistance[CHANNEL_THERM], temperatures)

            values = [ time.strftime("%Y-%m-%d %H:%M:%S"),
                int(avg_reading[CHANNEL_THERM]),
                int(resistance[CHANNEL_THERM]),
                voltage[CHANNEL_THERM],
                temperature,
                int(avg_reading[CHANNEL_PHOTO]),
                int(resistance[CHANNEL_PHOTO]),
                voltage[CHANNEL_PHOTO] ]
            print "%-19s %6d %6d %6.2f %9.1f %6d %6d %6.2f" % tuple(values)
            elapsed_secs = 0.0
            avg_reading = [ 0.0 ] * NUM_CHANNELS
            count = 0

            ### Google Sheets integration
            subprocess.call( [ './upload_sensordata.py' ] + [ str(x) for x in values ] )

        time.sleep(1.0)

if __name__ == '__main__':
    try:
        poll_channels()
    except:
        GPIO.cleanup()
        raise
