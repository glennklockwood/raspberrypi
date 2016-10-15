#!/usr/bin/env python

import random
import time
import spi

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

### Fill columns 5-8 with a random pattern
while True:
    for column in range(1,9):
        register_addr = column << 8
        value = random.randint(0, 2**8-1)
        max7219.put(register_addr|value,12)
    time.sleep(0.2)
