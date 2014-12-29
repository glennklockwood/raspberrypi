#!/usr/bin/env python
#
#  Wait for a button to be pressed on _PIN_IN.  When the button is pressed, 
#  illuminate the LED on _PIN_OUT as well as take a photo with the picamera 
#

import RPi.GPIO as GPIO
import picamera
import time

GPIO.setmode( GPIO.BCM )

_PIN_IN  =  4
_PIN_OUT = 17

GPIO.setup( _PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP )
GPIO.setup( _PIN_OUT, GPIO.OUT )

camera = picamera.PiCamera()
camera.start_preview()

while GPIO.input( _PIN_IN ):
    pass

GPIO.output( _PIN_OUT, True )
camera.capture( 'camera.jpg' )
print "writing output to 'camera.jpg'"
time.sleep(0.5)
GPIO.output( _PIN_OUT, False )

GPIO.cleanup()
