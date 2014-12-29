#!/usr/bin/env python
#
#  Light up an LED on GPIO pin 7 for thirty seconds
#

import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BOARD )
GPIO.setup( 7, GPIO.OUT )
GPIO.output( 7, True )
time.sleep(30)
GPIO.output( 7, False )
GPIO.cleanup()
