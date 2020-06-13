#!/usr/bin/env python3
"""Displays a letter that rotates based on HAT orientation"""

import time
import random

import sense_hat

sense = sense_hat.SenseHat()

while True:
    gforce = sense.get_accelerometer_raw()
    if gforce['x'] < -0.5:
        rotate = 90
    elif gforce['x'] > 0.5:
        rotate = 270
    elif gforce['y'] > 0.5:
        rotate = 0
    elif gforce['y'] < 0.5:
        rotate = 180
    else:
        rotate = 0
    sense.set_rotation(rotate)
    sense.show_letter("J",
        text_colour=[random.randint(128,192) for x in range(3)],
        back_colour=[random.randint(0,64) for x in range(3)],
    )
    print(rotate, gforce)
    time.sleep(0.25)
