#!/usr/bin/env python
#
#  Light up GPIO pins.  Useful for figuring out how a prototype is wired
#  after assembly.
#

import RPi.GPIO as GPIO

all_pins = [ 17, 27, 22, 5, 6, 13, 23, 24, 25, 12, 4 ]

GPIO.setmode( GPIO.BCM )
GPIO.setup( all_pins, GPIO.OUT, initial=GPIO.LOW )

last_pin = None
try:
    while True:
        pin_num = int(raw_input("What pin would you like to activate? "))
        if pin_num not in all_pins:
            print "That is not a valid pin number."
            continue

        if last_pin is not None:
            print "Bringing pin %d low..." % last_pin
            GPIO.output(last_pin, GPIO.LOW)

        print "Bringing pin %d high..." % pin_num
        GPIO.output(pin_num, GPIO.HIGH)

        last_pin = pin_num

except:
    print "Cleaning up!"
    GPIO.cleanup()
    raise
