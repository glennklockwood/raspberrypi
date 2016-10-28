#!/usr/bin/env python
#
import time
import spi.mcp41010
from RPi import GPIO

SPI_MOSI = 26
SPI_CS   = 13
SPI_CLK  = 19

def main():
    mcp41010 = spi.mcp41010.MCP41010(clk=SPI_CLK, cs=SPI_CS, mosi=SPI_MOSI, miso=None, verbose=True)

    for value in range( (1 << 8) ):
        mcp41010.set_value(value)
        time.sleep(0.01)

    try:
        input("Press return to continue ")
    except:
        pass

if __name__ == '__main__':
    main()
