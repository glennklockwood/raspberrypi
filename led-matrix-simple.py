#!/usr/bin/env python
"""
Change the state of a single LED in an 8x8 matrix.
"""

import spi

### Initialize an SPI connection using BCM-mode pins 21, 20, and 16
max7219 = spi.SPI(clk=21, cs=20, mosi=16, miso=None, verbose=True)

### Zero out all registers
for cmd in range(16):
    packet = cmd << 8
    max7219.put(packet,12)

### Set the scan limit register and disable shutdown mode
max7219.put(int("101100000111",2),12)
max7219.put(int("110000000001",2),12)

### We zeroed out all registers, so all LEDs are off (0)
led_state = [0]*64

def set_led(row, column, state):
    ### update our saved state
    led_state[column*8 + row] = state

    ### convert the new column into an SPI command
    register = (column+1) << 8
    value = 0
    for row in range(8):
        value <<= 1
        if led_state[column*8+row]:
            value |= 1

    max7219.put(register|value,12)

while True:
    row, col, state = input("Enter a row, col, state: ")
    set_led(row, col, state)
