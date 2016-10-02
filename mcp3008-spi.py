#!/usr/bin/env python
"""
Functions to communicate with the MCP3008 ADC using software-implemented SPI.
The SPI functions are general enough to be useful for other chips as well.
"""

import sys
from RPi import GPIO

_DEBUG = True

_SPI_CLK  = 18
_SPI_MISO = 23
_SPI_MOSI = 24
_SPI_CS   = 25

def _vprint(msg):
    """print messages only when debugging is enabled"""
    if _DEBUG:
        sys.stderr.write(msg + "\n")

def spi_init(pin_clk=_SPI_CLK, pin_cs=_SPI_CS):
    """ensure that the slave select is low and clock is reset"""
    GPIO.output(pin_cs, GPIO.HIGH)
    GPIO.output(pin_cs, GPIO.LOW)
    GPIO.output(pin_clk, GPIO.LOW)

def spi_finalize(pin_clk=_SPI_CLK, pin_cs=_SPI_CS):
    """ensure that the slave select is high and clock is reset"""
    GPIO.output(pin_cs, GPIO.HIGH)
    GPIO.output(pin_clk, GPIO.LOW)

def spi_put(data, bits, pin_clk=_SPI_CLK, pin_mosi=_SPI_MOSI):
    """send a bit vector of a given length over MOSI"""
    data_buf = data
    for _ in range(bits):
        if data_buf & (2**(bits-1)):
            GPIO.output(pin_mosi, GPIO.HIGH)
        else:
            GPIO.output(pin_mosi, GPIO.LOW)
        _vprint("  {:-12b}".format(2**(bits-1)))
        _vprint("& {:-12b} = {:12b}".format(data_buf, data_buf & (2**(bits-1))))
        data_buf <<= 1
        GPIO.output(pin_clk, GPIO.HIGH)
        GPIO.output(pin_clk, GPIO.LOW)
    return

def spi_get(bits, pin_clk=_SPI_CLK, pin_miso=_SPI_MISO):
    """get a bit vector of a given length via MISO"""
    data_buf = 0x0

    for _ in range(bits):
        GPIO.output(pin_clk, GPIO.HIGH)
        GPIO.output(pin_clk, GPIO.LOW)
        data_buf <<= 1
        if GPIO.input(pin_miso):
            data_buf |= 0x1

    return data_buf

def print_bin(data, bits):
    """convert a bit vector to a string"""
    msg = ""
    data_buf = data
    for _ in range(bits):
        if data_buf & (2**(bits-1)):
            msg += "1"
        else:
            msg += "0"
        data_buf <<= 1
    return msg

def mcp3008_get(channel):
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

    spi_init()

    ### 0x18 = 11000 = start bit (1), single-ended mode (1), and channel 0 (000)
    cmd = 0x18 | channel
    spi_put(cmd, 5)
    print "Sent config header [%s]" % print_bin(cmd, 5)

    ### get 1 NULL bit + 10 data bits in MSR order
    bits = 11
    data_buf = spi_get(bits)
    print "Received [%4d] [%s]" % (data_buf, print_bin(data_buf, bits))

    ### mask off the most significant bit (NULL bit) just in case it's nonzero
    bits &= ~(2**(bits-1))
    print "Decoded  [%4d] [%s]" % (data_buf, print_bin(data_buf, bits))

    spi_finalize()

def main( args ):
    if len(args) == 0:
        use_channel = 0
    else:
        use_channel = int(args[0])

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(_SPI_MOSI, GPIO.OUT)
    GPIO.setup(_SPI_MISO, GPIO.IN)
    GPIO.setup(_SPI_CLK, GPIO.OUT)
    GPIO.setup(_SPI_CS, GPIO.OUT)

    try:
        print "Using channel %d" % use_channel
        mcp3008_get(use_channel)
    except:
        GPIO.cleanup()
        raise

    GPIO.cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])
