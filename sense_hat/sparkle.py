#!/usr/bin/env python3
"""Makes the LED matrix sparkle with random colors"""

import math
import random
import time

import sense_hat

sense = sense_hat.SenseHat()
sense.clear()

while True:
    for i in range(random.randint(0, 8)):
        color = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ]
        length = math.sqrt(sum([x*x for x in color]))
        color = [int(255 * x / length) for x in color]

        sense.set_pixel(
            random.randint(0, 7),
            random.randint(0, 7),
            color[0], color[1], color[2])
    time.sleep(0.10)
