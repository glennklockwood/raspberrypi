#!/usr/bin/env python
"""
Simple code to illustrate the basics of working with a 16x2 LCD character
display driven by a HD44780 controller chip.

Glenn K. Lockwood, November 2016
"""

import sys
import time
import RPi.GPIO as GPIO

PIN_RS = 27
PIN_EN = 22
PIN_D = [ 12, 16, 20, 21, 18, 23, 24, 25 ]

DELAY = 1.0e-3 # in seconds

def pulse_clock():
    """pulse the EN pin high and low.  delays are required because the chip
    cannot handle very high frequency inputs"""
    time.sleep(DELAY)
    GPIO.output(PIN_EN, GPIO.HIGH)
    time.sleep(DELAY)
    GPIO.output(PIN_EN, GPIO.LOW)
    time.sleep(DELAY)

def write4(value):
    """
    special function to send only the four highest-order bits; low-order bits
    remain floating
    """
    GPIO.output(PIN_RS, GPIO.LOW)

    time.sleep(1e-3)

    GPIO.output(PIN_D[4], GPIO.HIGH if ((value >> 0) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[5], GPIO.HIGH if ((value >> 1) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[6], GPIO.HIGH if ((value >> 2) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[7], GPIO.HIGH if ((value >> 3) & 1) > 0 else GPIO.LOW)
    pulse_clock()

def write8_4bitmode(value, rs_value):
    """send an 8-bit message using the 4-bit interface; pulse EN between the
    four most significant bits and four least significant bits"""
    GPIO.output(PIN_RS, rs_value)

    time.sleep(1e-3)

    GPIO.output(PIN_D[4], GPIO.HIGH if ((value >> 4) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[5], GPIO.HIGH if ((value >> 5) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[6], GPIO.HIGH if ((value >> 6) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[7], GPIO.HIGH if ((value >> 7) & 1) > 0 else GPIO.LOW)
    pulse_clock()

    GPIO.output(PIN_D[4], GPIO.HIGH if ((value >> 0) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[5], GPIO.HIGH if ((value >> 1) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[6], GPIO.HIGH if ((value >> 2) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[7], GPIO.HIGH if ((value >> 3) & 1) > 0 else GPIO.LOW)
    pulse_clock()

def write8_8bitmode(value, rs_value):
    """send an 8-bit message using the 8-bit interface"""
    GPIO.output(PIN_RS, rs_value)

    time.sleep(1e-3)

    GPIO.output(PIN_D[0], GPIO.HIGH if ((value >> 0) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[1], GPIO.HIGH if ((value >> 1) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[2], GPIO.HIGH if ((value >> 2) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[3], GPIO.HIGH if ((value >> 3) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[4], GPIO.HIGH if ((value >> 4) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[5], GPIO.HIGH if ((value >> 5) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[6], GPIO.HIGH if ((value >> 6) & 1) > 0 else GPIO.LOW)
    GPIO.output(PIN_D[7], GPIO.HIGH if ((value >> 7) & 1) > 0 else GPIO.LOW)
    pulse_clock()

def init_4bitmode():
    """initialize chip into 4-bit interface mode"""
    ### initialization magic reset sequence - use a special 4-bit write function

    write4(int("0011", 2))
    write4(int("0011", 2))
    write4(int("0011", 2))
    write4(int("0010", 2))

    ### send the "function set" command to configure display dimensions
    write8_4bitmode(int("00101100",2), rs_value=GPIO.LOW)
    
    ### send the "display on/off control" command (1000) to power on the
    ### display (100), enable cursor (010), and enable cursor blink (001)
    write8_4bitmode(int("00001111",2), rs_value=GPIO.LOW)

    ### clear the display
    write8_4bitmode(int("00000001",2), rs_value=GPIO.LOW)

    ### send the "entry mode set" command to set left-to-right printing (110)
    write8_4bitmode(int("00000110",2), rs_value=GPIO.LOW)

def init_8bitmode():
    """initialize chip into 4-bit interface mode"""
    ### initialization magic reset sequence
    write8_8bitmode(int("00110000", 2), rs_value=GPIO.LOW)
    write8_8bitmode(int("00110000", 2), rs_value=GPIO.LOW)
    write8_8bitmode(int("00110000", 2), rs_value=GPIO.LOW)

    ### send the "function set" command
    write8_8bitmode(int("00111100",2), rs_value=GPIO.LOW)
    
    ### send the "display on/off control" command
    write8_8bitmode(int("00001111",2), rs_value=GPIO.LOW)

    ### clear the display
    write8_8bitmode(int("00000001",2), rs_value=GPIO.LOW)

    ### send the "entry mode set" command
    write8_8bitmode(int("00000110",2), rs_value=GPIO.LOW)

def printmsg_4bitmode(msg):
    """write the message one character at a time"""
    for c in msg:
        write8_4bitmode(ord(c), rs_value=GPIO.HIGH)

def printmsg_8bitmode(msg):
    """write the message one character at a time"""
    for c in msg:
        write8_8bitmode(ord(c), rs_value=GPIO.HIGH)

if __name__ == '__main__':
    GPIO.setmode( GPIO.BCM )
    GPIO.setup([PIN_RS, PIN_EN] + PIN_D[4:8], GPIO.OUT, initial=GPIO.LOW )
    try:
        init_4bitmode()
        printmsg_4bitmode(sys.argv[1])
#   GPIO.setup([PIN_RS, PIN_EN] + PIN_D[0:8], GPIO.OUT, initial=GPIO.LOW )
#   try:
#       init_8bitmode()
#       printmsg_8bitmode(sys.argv[1])
    except:
        GPIO.cleanup()
        raise
    GPIO.cleanup()
