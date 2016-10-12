#!/usr/bin/env python
#

import time
import mcp3008spi
from RPi import GPIO
import numpy as np

SPI_MOSI = 16
SPI_CS = 20
SPI_CLK = 21

def apply_cols( value, delay=0.0 ):
    """Apply a pattern to each column"""
    for col in range(8):
        cmd = (col+1) << 8
        cmd |= value
        mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
        mcp3008spi.spi_put(cmd, 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
        mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)
        if delay > 0.0:
            time.sleep(delay)

def apply_rows( value, delay=0.0 ):
    """Apply a pattern to each row"""
    value_state = value
    row_state = 0
    print "++++++++"
    for row in range(8):
        mask = 2**row
        if (value & mask) != 0:
            row_state |= mask
        value_state <<= 1

        for col in range(8):
            cmd = (col+1) << 8
            cmd |= row_state
            mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
            mcp3008spi.spi_put(cmd, 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
            mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

        if delay > 0.0:
            print "--------"
            time.sleep(delay)

def apply_matrix( matrix, delay=0.0 ):
    for col in range(8):
        cmd = (col+1) << 8
        values = 0
        for i in np.flipud(matrix[:,col]):
            values <<= 1
            if i != 0:
                values |= 1

        mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
        mcp3008spi.spi_put(cmd|values, 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
        mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)
        if delay > 0.0:
            time.sleep(delay)

def main():
    mcp3008spi.DEBUG = True

    ### Disable code B decode mode on all digits
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("100100000000",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

    ### Set intensity low
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("101000000001",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

    ### Enable all digits in scan-limit register
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("101100000111",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

    ### Disable shutdown mode
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("110000000001",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

    ### Enable test mode
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("111100000001",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

    try:
        input("Everything should be on now.  Press any key to continue.")
    except:
        pass

    ### Disable test mode
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("111100000000",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

    ### Set all LEDs to off
    apply_cols(int("00000000",2))

    ### Enable each "digit" one by one
    apply_cols(int("10010101",2), delay=0.1)
    time.sleep(1.0)

    ### Enable everything
    apply_cols(2**8-1)
    time.sleep(5.0)

    ### Enable each row one by one
    apply_rows(int("10010101",2), delay=0.1)
    time.sleep(1.0)

    ### Enable a specific set of LEDs
    ### Go into smiley face loop
    smiley = np.array( [
        [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 1, 1, 0, 0, 1, 1, 0 ],
        [ 0, 1, 1, 0, 0, 1, 1, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 0, 0, 0, 0, 1, 1 ],
        [ 0, 1, 1, 0, 0, 1, 1, 0 ],
        [ 0, 0, 1, 1, 1, 1, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        ] )

    try:
        while True:
            apply_matrix( smiley, delay=0.0 )
            time.sleep(1.0)
            smiley = abs(smiley -1)
    except KeyboardInterrupt:
        pass

    ### Enable shutdown mode
    mcp3008spi.spi_init(pin_clk=SPI_CLK, pin_cs=SPI_CS, pin_mosi=SPI_MOSI, pin_miso=None)
    mcp3008spi.spi_put(int("110000000000",2), 16, pin_clk=SPI_CLK, pin_mosi=SPI_MOSI)
    mcp3008spi.spi_finalize(pin_clk=SPI_CLK, pin_cs=SPI_CS)

if __name__ == '__main__':
    try:
        main()
    except:
        print "Cleaning up..."
        GPIO.cleanup()
        raise

    GPIO.cleanup()
