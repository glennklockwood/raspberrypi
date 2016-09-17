#!/usr/bin/env python
#
#  Light up an LED on GPIO pin 7 for thirty seconds
#

import RPi.GPIO as GPIO
import time

dark_to_light = [ 19, 20, 21 ]

GPIO.setmode( GPIO.BCM )
GPIO.setup( dark_to_light, GPIO.OUT, initial=GPIO.LOW )

try:
    i = 0
    while True:
        pin = dark_to_light[i]

        GPIO.output( pin, GPIO.HIGH )
#       print "Activating pin %d" % pin
        time.sleep(0.5)
        GPIO.output( pin, GPIO.LOW )
        i = (i + 1) % len(dark_to_light)
except KeyboardInterrupt:
    print "Cleaning up!"
    GPIO.cleanup()
