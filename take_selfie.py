#!/usr/bin/env python
#
# Turn on an LED and then take a photo of it (if the camera is positioned 
# correctly)
#

import time
import picamera
import RPi.GPIO as GPIO

### Set up camera
camera = picamera.PiCamera()

### Set up GPIO
GPIO.setmode( GPIO.BOARD )
GPIO.setup( 7, GPIO.OUT )

### Do some magic
GPIO.output( 7, True )
camera.start_preview()
time.sleep(10)
camera.capture('hello.jpg')
GPIO.output( 7, False )

### Clean up
GPIO.cleanup()
