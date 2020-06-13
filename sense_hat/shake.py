#!/usr/bin/env python3
"""Gets mad if the Raspberry Pi gets rattled too much and turns the LED matrix
red."""

import math

import sense_hat

sense = sense_hat.SenseHat()
sense.set_rotation(180)
sense.clear()

RED = (255, 0, 0)

while True:
    gforces = sense.get_accelerometer_raw()
    mag = 0.0
    for gforce in gforces.values():
        mag += gforce * gforce

    if math.sqrt(mag) > 1.05:
        sense.clear(RED)
    else:
        sense.clear()
