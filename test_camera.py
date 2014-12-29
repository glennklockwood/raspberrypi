#!/usr/bin/env python
#
#  Open the camera's preview window and cycle up the brightness
#

import picamera
import time

with picamera.PiCamera() as camera:
    camera.start_preview()
    try:
        for i in range(100):
            camera.brightness = i
            time.sleep( 0.2 )
    finally:
        camera.stop_preview()
