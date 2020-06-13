#!/usr/bin/env python3
"""Displays environmental measurements on LED matrix"""

import time

import sense_hat

sense = sense_hat.SenseHat()
sense.set_rotation(180)

SCROLL_SPEED = 0.04

while True:
    pressure_mbar = sense.get_pressure()
    pressure_atm = pressure_mbar / 1013.25
    message = "%.2f mbar" % pressure_mbar
    sense.show_message(message, scroll_speed=SCROLL_SPEED)

    # temp = sense.get_temperature_from_humidity()
    # message = "%1.f C (from humidity sensor)" % temp
    temp = sense.get_temperature()
    message = "%1.f C" % temp
    sense.show_message(message, scroll_speed=SCROLL_SPEED)

    # temp = sense.get_temperature_from_pressure()
    # message = "%.1f C (from pressure sensor)" % temp
    # sense.show_message(message, scroll_speed=SCROLL_SPEED)

    humidity = sense.get_humidity()
    message = "%.1f %% humidity" % humidity
    sense.show_message(message, scroll_speed=SCROLL_SPEED)
