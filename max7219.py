#!/usr/bin/env python
#

import time
import spi
from RPi import GPIO
import numpy as np

SPI_MOSI = 16
SPI_CS = 20
SPI_CLK = 21

def apply_cols(spicomm, value, delay=0.0):
    """Apply a pattern to each column"""
    for col in range(8):
        cmd = (col+1) << 8
        cmd |= value
        spicomm.put(cmd, 16)
        if delay > 0.0:
            time.sleep(delay)

def apply_rows(spicomm, value, delay=0.0):
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
            spicomm.put(cmd, 16)

        if delay > 0.0:
            print "--------"
            time.sleep(delay)

def apply_matrix(spicomm, matrix, delay=0.0):
    for col in range(8):
        cmd = (col+1) << 8
        values = 0
        for i in np.flipud(matrix[:,col]):
            values <<= 1
            if i != 0:
                values |= 1

        spicomm.put(cmd|values, 16)
        if delay > 0.0:
            time.sleep(delay)

def set_coordinate(spicomm, pos, state):
    """
    Given an x, y tuple (pos), set the state for that LED.  Because entire
    columns are addressed at once, we have to set the state of the whole column
    in changing the one LED though.  This shortcoming could be addressed by
    retaining the LED matrix state in this application.

    Remember that row addresses start at 1 (e.g., digit 0's address is 0001)
    """
    x = pos[0]
    y = pos[1]
    ### we use x-1 because digit address 0 begins at address 1
    register_addr = (x+1) << 8
    register_val = state
    for _ in range(y):
        register_val <<= 1
    spicomm.put(register_addr|register_val, 12)


def run_demo(spicomm):
    """
    Light up specific patterns
    """
    ### Enable test mode
    spicomm.put(int("111100000001",2), 16)
    time.sleep(1.0)

    ### Disable test mode
    spicomm.put(int("111100000000",2), 16)

    ### Set all LEDs to off
    apply_cols(spicomm, int("00000000",2))

    ### Enable each "digit" one by one
    apply_cols(spicomm, int("10010101",2), delay=0.1)
    time.sleep(1.0)

    ### Enable everything
    apply_cols(spicomm, 2**8-1)
    time.sleep(1.0)

    ### Enable each row one by one
    apply_rows(spicomm, int("10010101",2), delay=0.1)
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

    ### Show a smiley face, then an inverse smiley face
    try:
        while True:
            apply_matrix(spicomm, smiley, delay=0.1)
            time.sleep(1.0)
            smiley = abs(smiley -1)
    except KeyboardInterrupt:
        pass

    ### Raster a single illuminated LED
    try:
        while True:
            state = [0] * 64
            for i in range(64):
                state[i-1] = 0
                state[i] = 1
                apply_matrix(spicomm, np.reshape(state,(8,8)))
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    try:
        input("Press any key to shut down.")
    except:
        pass

def run_coordinate_setter(spicomm):
    try:
        while True:
            xy = input("Enter x, y position to illuminate:")
            if isinstance(xy, tuple):
                x, y = xy
            else:
                x, y = xy.split()
            set_coordinate(spicomm, (x,y), 1)
    except KeyboardInterrupt:
        pass

def run_pulse(spicomm, delay=0.1,max_intensity=16):
    ### Enable everything
    apply_cols(spicomm, 2**8-1)

    state = np.array( [
        [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 1, 1, 0, 0, 1, 1, 0 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 0, 1, 1, 1, 1, 1, 1, 0 ],
        [ 0, 0, 1, 1, 1, 1, 0, 0 ],
        [ 0, 0, 0, 1, 1, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        ] )

    ### Show a smiley face, then an inverse smiley face
    apply_matrix(spicomm, state)

    try:
        while True:
            ### Circular loop over intensities
            for value in range(max_intensity) + range(max_intensity-2,0,-1):
                cmd = int("1010",2) << 8
                spicomm.put(cmd|value, 12)
                time.sleep(delay)
    except KeyboardInterrupt:
        pass


def main():
    max7219 = spi.SPI(clk=SPI_CLK, cs=SPI_CS, mosi=SPI_MOSI, miso=None, verbose=True)

    ### Disable code B decode mode on all digits
    max7219.put(int("100100000000",2), 16)

    ### Set intensity low
    max7219.put(int("101000000000",2), 16)

    ### Enable all digits in scan-limit register
    max7219.put(int("101100000111",2), 16)

    ### Disable test mode
    max7219.put(int("111100000000",2), 16)

    ### Disable shutdown mode
    max7219.put(int("110000000001",2), 16)

#   run_demo(max7219)
#   run_coordinate_setter(max7219)
    run_pulse(max7219, delay=0.1, max_intensity=6)

    ### Enable shutdown mode
    max7219.put(int("110000000000",2), 16)

if __name__ == '__main__':
    main()
