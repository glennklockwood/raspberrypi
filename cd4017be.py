#!/usr/bin/env python
#
#  Replicate the behavior of the CD4017BE CMOS Counter/Divider by Texas
#  Instruments.  Implemented based on the data sheet at
#
#       http://www.ti.com/lit/ds/symlink/cd4017b.pdf
#
#  Glenn K. Lockwood, September 2016

import sys
import time
import RPi.GPIO as GPIO

_VERBOSE = False
_VERBOSE_T0 = time.time()

### Map pins on CD4017BE to RPi GPIO BCM pins
PINS = {
    "output0": {
        "ic_pin": 3,
        "gpio_pin": 22,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output1": {
        "ic_pin" : 2,
        "gpio_pin": 17,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output2": {
        "ic_pin": 4,
        "gpio_pin": 5,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output3": {
        "ic_pin": 7,
        "gpio_pin": 6,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output4": {
        "ic_pin": 10,
        "gpio_pin": 13,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output5": { 
        "ic_pin": 1,
        "gpio_pin": 12,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output6": {
        "ic_pin": 5,
        "gpio_pin": 25,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output7": {
        "ic_pin": 6,
        "gpio_pin": 24,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output8": {
        "ic_pin": 9,
        "gpio_pin": 27,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "output9": {
        "ic_pin": 11,
        "gpio_pin": 23,
        "io": GPIO.OUT,
        "pud": GPIO.PUD_DOWN,
    },
    "carry_out": {
        "ic_pin": 12,
        "gpio_pin": None,
        "io": None,
        "pud": None,
    },
    "clock_inhibit": {
        "ic_pin": 13,
        "gpio_pin": None,
        "io": GPIO.IN,
        "pud": GPIO.PUD_DOWN,
    },
    "clock": {
        "ic_pin": 14,
        "gpio_pin": 4,
        "io":  GPIO.IN,
        "pud": GPIO.PUD_DOWN,
    },
    "reset": {
        "ic_pin": 15,
        "gpio_pin": None,
        "io": None,
        "pud": None,
    },
    "vdd": {
        "ic_pin": 16,
        "gpio_pin": None,
        "io": None,
        "pud": None,
    },
    "vss": {
        "ic_pin": 8,
        "gpio_pin": None,
        "io": None,
        "pud": None,
    },
}

def vprint( text ):
    if _VERBOSE:
        print "%.6f %s" % ( (time.time() - _VERBOSE_T0), text )

def configure_gpio():
    """Configure all the pins we will use"""
    GPIO.setmode( GPIO.BCM )
    num_outputs = 0
    for pin_name, pin_config in PINS.iteritems():
        if pin_config['gpio_pin'] is not None:
            if pin_config['io'] == GPIO.IN:
                GPIO.setup(pin_config['gpio_pin'], pin_config['io'], pull_up_down=pin_config['pud'])
            else:
                GPIO.setup(pin_config['gpio_pin'], pin_config['io'])
            vprint("Configured GPIO pin %d" % pin_config['gpio_pin'])
        if pin_name.startswith('output'):
            num_outputs += 1

    return num_outputs

def activate_ic( num_outputs ):
    counter = 0
    while True:
        pin_clock = PINS['clock']['gpio_pin']
        pin_clock_inhibit = PINS['clock_inhibit']['gpio_pin']
        pin_carry_out = PINS['carry_out']['gpio_pin']
        pin_reset = PINS['reset']['gpio_pin']

        try:
            GPIO.wait_for_edge( pin_clock, GPIO.FALLING )
        except:
            break

        ### Inhibit pin prevents any action from happening when high
        if pin_clock_inhibit is not None and GPIO.input( pin_clock_inhibit ):
            continue

        ### Reset pin resets the running counter
        if pin_reset is not None and GPIO.input( pin_reset ):
            counter = 0
    
        ### Deactivate the previous count's pin
        pin_key = 'output%d' % counter
        GPIO.output( PINS[pin_key]['gpio_pin'], GPIO.LOW )

        counter = (counter + 1) % num_outputs

        ### Activate the new count's pin
        pin_key = 'output%d' % counter
        GPIO.output( PINS[pin_key]['gpio_pin'], GPIO.HIGH )

        ### If we just overflowed the counter, send out the carry out signal
        if counter == 0 and pin_carry_out is not None:
            GPIO.output( pin_carry_out, GPIO.HIGH )
            GPIO.output( pin_carry_out, GPIO.LOW)

        vprint("detected CLK; illuminated GPIO pin %d" % PINS[pin_key]['gpio_pin'] )

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        _VERBOSE = True

    num_outputs = configure_gpio()
    activate_ic( num_outputs )

    vprint("cleaning up")
    GPIO.cleanup()
