#!/usr/bin/env python3

import time

import sense_hat

sense = sense_hat.SenseHat()

pressure_mbar = sense.get_pressure()
pressure_atm = pressure_mbar / 1013.25
print("%.4f atm" % pressure_atm)

temp = sense.get_temperature_from_humidity()
print("%1.f C from humidity sensor" % temp)

temp = sense.get_temperature_from_pressure()
print("%.1f C from pressure sensor" % temp)

humidity = sense.get_humidity()
print("%.1f %% rel humidity" % humidity)
