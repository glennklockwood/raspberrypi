#!/usr/bin/env python
#
import time
import spi.mcp41010
from RPi import GPIO

SPI_MOSI = 26
SPI_CS   = 13
SPI_CLK  = 19

def pulse_led(low_val=(1 << 6), high_val=(1 << 7), step=1):
    """
    Pulse an LED connect to an MCP41010 digital potentiometer and a 220 ohm
    resistor.
    """
    mcp41010 = spi.mcp41010.MCP41010(clk=SPI_CLK, cs=SPI_CS, mosi=SPI_MOSI, miso=None, verbose=False)

    while True:
        ### pulse from a lower resistance to a higher one
        for value in range(low_val, high_val, step):
            mcp41010.set_value(value)
            time.sleep(0.01)
        ### pulse from a higher resistance back to a lower one
        for value in range(high_val, low_val, -1 * step):
            mcp41010.set_value(value)
            time.sleep(0.01)

def scale_range():
    """
    Cycle through every value that the MCP41010 is capable of using
    """
    mcp41010 = spi.mcp41010.MCP41010(clk=SPI_CLK, cs=SPI_CS, mosi=SPI_MOSI, miso=None, verbose=True)

    for value in range( (1 << 8) ):
        mcp41010.set_value(value)
        time.sleep(0.01)

    try:
        input("Press return to continue ")
    except:
        pass

if __name__ == '__main__':
    try:
        pulse_led()
    except KeyboardInterrupt:
        pass
