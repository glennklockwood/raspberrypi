#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys

BITS = 4

PIN_RS = 27
# PIN_RW = grounded
PIN_EN = 22
PIN_D = [ 12, 16, 20, 21, 18, 23, 24, 25 ]

pin_names = {
    PIN_RS: "rs",
    PIN_EN: "en",
    PIN_D[0]: "d0",
    PIN_D[1]: "d1",
    PIN_D[2]: "d2",
    PIN_D[3]: "d3",
    PIN_D[4]: "d4",
    PIN_D[5]: "d5",
    PIN_D[6]: "d6",
    PIN_D[7]: "d7"
}

DELAY = 1e-6
DELAY = 1e-1

def clock( ):
    time.sleep(DELAY)
    GPIO.output(PIN_EN, GPIO.HIGH)
    time.sleep(DELAY)
    GPIO.output(PIN_EN, GPIO.LOW)
    time.sleep(DELAY)


def write8( value, rs_val=GPIO.LOW ):

    signal = [ ((value >> 0) & 1) > 0,  # least significant bit (LSB)
               ((value >> 1) & 1) > 0,
               ((value >> 2) & 1) > 0,
               ((value >> 3) & 1) > 0,
               ((value >> 4) & 1) > 0,
               ((value >> 5) & 1) > 0,
               ((value >> 6) & 1) > 0,
               ((value >> 7) & 1) > 0 ] # most significant bit (MSB)

    ### print MSB -> LSB
    print "".join( ["1 " if rs_val else "0 "] + [ "1" if x else "0" for x in reversed(signal) ])

    GPIO.output(PIN_RS, rs_val)
    sys.stdout.write( "%d rs=%d " % ( BITS, int(rs_val) ) )

    time.sleep(1e-3)

    GPIO.output(PIN_D[4:8], signal[4:8])
    for i in range(4,8):
        sys.stdout.write( "%2s=%1d " % (pin_names[PIN_D[i]], signal[i]))

    if BITS == 4:
        clock()
        GPIO.output( PIN_D[4:8], signal[0:4] )
        sys.stdout.write(" CLK\n")
        for i in range(4,8):
            sys.stdout.write( "%2s=%1d " % (pin_names[PIN_D[i]], signal[i-4]))


    else:
        GPIO.output( PIN_D[0:4], signal[0:4] )
        for i in range(0,4):
            sys.stdout.write( "%2s=%1d, " % (pin_names[PIN_D[i]], signal[i]))

    clock()
    sys.stdout.write(" CLK\n")

def prog_printmsg():
    if BITS == 4:
        write8(int("00101000",2))
    else:
        write8(int("00111000",2))

    write8(int("00001111",2))

    write8(int("00000110",2))

    write8(int("00000001",2))

    if len(sys.argv) < 2:
        msg = "Hello world"
    else:
        msg = sys.argv[1]

    for c in msg:
        write8(ord(c), GPIO.HIGH)

def prog_arbitrary():

    print "Initialization:"
    print "0 00101000 (4-bit)"
    print "0 00111000 (8-bit)"
    print "0 00001111"
    print "0 00000110"
    print "0 00000001"
    while True:
        new = raw_input("rs d7..d0:")
        tmp = new.split()
        if len(tmp) > 1:
            rs_val = int(tmp[0])
            value = int(tmp[1], 2)
            write8(value, rs_val)
        else:
            break

if __name__ == '__main__':
    GPIO.setmode( GPIO.BCM )

    if BITS == 4:
        GPIO.setup([PIN_RS, PIN_EN] + PIN_D[4:8], GPIO.OUT, initial=GPIO.LOW )
    else:
        GPIO.setup([PIN_RS, PIN_EN] + PIN_D[0:8], GPIO.OUT, initial=GPIO.LOW )

    try:
        prog_printmsg()
#       prog_arbitrary()
    except:
        GPIO.cleanup()
        raise
    GPIO.cleanup()
