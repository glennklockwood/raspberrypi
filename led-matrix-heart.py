#!/usr/bin/env python

import random
import time
import spi
import numpy as np

### Initialize an SPI connection using BCM-mode pins 21, 20, and 16
max7219 = spi.SPI(clk=21, cs=20, mosi=16, miso=None)

### Zero out all registers
for cmd in range(16):
    packet = cmd << 8
    max7219.put(packet,12)

### Enable all columns via the scan limit register
max7219.put(int("101100000111",2),12)

### Disable shutdown mode
max7219.put(int("110000000001",2),12)

### Define the values for each column that gives us a heart shape
heart_shape = np.array( [
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 1, 1, 0, 0, 1, 1, 0 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 0, 1, 1, 1, 1, 1, 1, 0 ],
    [ 0, 0, 1, 1, 1, 1, 0, 0 ],
    [ 0, 0, 0, 1, 1, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    ] )

### Set each column according to our heart shape matrix
for col in range(8):
    cmd = (col+1) << 8
    values = 0
    ### Without flipud, the heart would be upside-down since the LED matrix
    ### defines 0,0 as the bottom left corner while numpy puts it at the top
    ### left.
    for i in np.flipud(heart_shape[:,col]):
        values <<= 1
        if i != 0:
            values |= 1
    max7219.put(cmd|values, 12)

### MAX7219 supports intensity up to 31, but that's REALLY bright
MAX_INTENSITY = 6
input_value = 0.0
while True:
    ### This math just makes the intensity pulse like a sine wave
    input_value += np.pi / MAX_INTENSITY
    value = int((np.sin(input_value)+1.0) * MAX_INTENSITY)

    ### 1010 is the LED intensity register
    cmd = int("1010",2) << 8
    max7219.put(cmd|value, 12)
    time.sleep(0.1)
