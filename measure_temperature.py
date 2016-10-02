#!/usr/bin/env python
#
#  Script to poll a thermistor attached through an ADC
#
 
import os
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

### define SPI pins
_SPI_CLK  = 18
_SPI_MISO = 23
_SPI_MOSI = 24
_SPI_CS   = 25

_SENSOR_CHANNEL = 0;

_SERIES_RESISTOR_OHMS = 10000.0

def read_adc(channel, clockpin, mosipin, misopin, cspin):
    """
    simple SPI reader--read a single value from a single channel

    Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015,
    released into the public domain
    """
    if ((channel > 7) or (channel < 0)):
        return -1

    GPIO.output(cspin, GPIO.HIGH)
    ### start clock low
    GPIO.output(clockpin, GPIO.LOW)
    ### bring CS low
    GPIO.output(cspin, GPIO.LOW)

    commandout = channel
    # start bit + single-ended bit
    commandout |= 0x18
    # we only need to send 5 bits here
    commandout <<= 3
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)

    adcout = 0

    ### read in one empty bit, one null bit, and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, GPIO.HIGH)

    # first bit is 'null' so drop it
    adcout >>= 1
    return adcout

def get_temperature( resistance, table ):
    """
    Interpolate temperature from temperature table
    """
    for i, r_t in enumerate(table):
        if r_t[0] > resistance:
            if i > 0:
                dx = r_t[0] - table[i-1][0]
                dy = r_t[1] - table[i-1][1]
                m = float(dy) / float(dx)
                return (resistance - table[i-1][0]) * m + table[i-1][1]
            else:
                return r_t[1]
        else:
            continue
    raise Exception( "R = %.2f out of bounds" % resistance )

def load_temperatures( filename ):
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
    if os.path.isfile( filename ):
        with open( filename, 'r' ) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith('#'): continue
                t_c, r_kohm = line.split()
                t_c = int(t_c)
                r_kohm = float(r_kohm) * 1000.0 # convert from kohm to ohm
                temperatures.append( (r_kohm, t_c) )
        temperatures = sorted( temperatures, key=lambda x: x[0] )
    print "Loaded %d values from temperature table" % len(temperatures)
    return temperatures

def main():
    ### configure SPI pins
    GPIO.setup(_SPI_MOSI, GPIO.OUT)
    GPIO.setup(_SPI_MISO, GPIO.IN)
    GPIO.setup(_SPI_CLK, GPIO.OUT)
    GPIO.setup(_SPI_CS, GPIO.OUT)

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "temperatures.txt"
    temperatures = load_temperatures(filename)

    avg_reading = 0.0
    n = 0
    print "%-19s %9s %9s %9s %9s" % ("Date", "Raw read", "Ohms", "Volts", "Temp(C)")
    while True:
        raw_reading = read_adc(_SENSOR_CHANNEL, _SPI_CLK, _SPI_MOSI, _SPI_MISO, _SPI_CS)
        avg_reading += raw_reading
        n += 1

        ### average over many samples
        if n == 60:
            avg_reading /= float(n)
            resistance = _SERIES_RESISTOR_OHMS / ( 1023.0 / avg_reading - 1.0 )
            voltage     = 3.3 * avg_reading / 1023.0
            temperature = get_temperature(resistance, temperatures)

            print "%-19s %9d %9d %9.2f %9.1f" % (
                time.strftime("%Y-%m-%d %H:%M:%S"),
                int(avg_reading),
                int(resistance),
                voltage,
                temperature )
            n = 0
            avg_reading = 0.0

        time.sleep(1.0)

if __name__ == '__main__':
    try:
        main()
    except:
        GPIO.cleanup()
        raise


