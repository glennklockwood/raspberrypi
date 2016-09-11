#!/usr/bin/env python
#
#  Basic demonstration of detecting a physical button press
#

import RPi.GPIO as GPIO
import time

# _PIN_IN = 7
# GPIO.setmode( GPIO.BOARD )
# GPIO.setup( _PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP )

_PIN_IN = 4
GPIO.setmode( GPIO.BCM )
GPIO.setup( _PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP )

while True:
    input_state = GPIO.input( _PIN_IN )
    if input_state == False:
        print( 'Button Pressed' )
        time.sleep(0.5)
