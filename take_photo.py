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

while True:
    while GPIO.input( _PIN_IN ):
        pass

    print "Button pressed!  Activating LED..."
    GPIO.output( _PIN_OUT, True )
    time.sleep(0.5)
    print "Taking photo and Writing output to 'camera.jpg'..."
    camera.capture( 'camera.jpg' )
    time.sleep(0.5)
    print "Deactivating LED and waiting for another button press."
    GPIO.output( _PIN_OUT, False )

GPIO.cleanup()
