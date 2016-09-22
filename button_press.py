#!/usr/bin/env python
#
#  Basic demonstration of detecting a physical button press using GPIO polling
#

import RPi.GPIO as GPIO
import time

_PIN_IN = 4
GPIO.setmode( GPIO.BCM )
GPIO.setup( _PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP )

try:
    while True:
        input_state = GPIO.input( _PIN_IN )
        if input_state == False:
            print 'button pressed'
            time.sleep(0.5)
except KeyboardInterrupt:
    print "cleaning up"
    GPIO.cleanup()
