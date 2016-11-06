#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
import argparse

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

def clock( ):
    time.sleep(DELAY)
    GPIO.output(PIN_EN, GPIO.HIGH)
    time.sleep(DELAY)
    GPIO.output(PIN_EN, GPIO.LOW)
    time.sleep(DELAY)

def write4( value, rs_val=GPIO.LOW ):
    signal = [ ((value >> 0) & 1) > 0,  # least significant bit (LSB)
               ((value >> 1) & 1) > 0,
               ((value >> 2) & 1) > 0,
               ((value >> 3) & 1) > 0 ] # most significant bit (MSB)
    print "".join( ["1 " if rs_val else "0 "] + [ "1" if x else "0" for x in reversed(signal) ])
    GPIO.output(PIN_RS, rs_val)
    sys.stdout.write( "rs=%d " % ( int(rs_val) ) )

    time.sleep(1e-3)

    GPIO.output(PIN_D[4:8], signal[0:4])
    for i in range(0,4):
        sys.stdout.write( "%2s=%1d " % (pin_names[PIN_D[i]], signal[i]))
    sys.stdout.write(" CLK\n")
    clock()

def write8( value, rs_val=GPIO.LOW, bits=None ):

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
    sys.stdout.write( "rs=%d " % ( int(rs_val) ) )

    time.sleep(1e-3)

    GPIO.output(PIN_D[4:8], signal[4:8])
    for i in range(4,8):
        sys.stdout.write( "%2s=%1d " % (pin_names[PIN_D[i]], signal[i]))

    if bits is None:
        bits = BITS
    if bits == 4:
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

def prog_printmsg(msg):
    ### see figure 23/figure 24 in datasheet for this initialization process
    # in the adafruit lib, they use 0x33 and 0x32, which when using the 4-bit
    # version of write8, actually translates to the correct initialization
    # sequence (0011----, 0011----, 0011----, 0010----)
    time.sleep(15.0e-3)
    write4(int("0011", 2))
    time.sleep(4.1e-3)
    write4(int("0011", 2))
    time.sleep(0.1e-3)
    write4(int("0011", 2))

    if BITS == 4:
        write4(int("0010",2))
        write8(int("00100000",2))
    else:
        write8(int("00110000",2))

    write8(int("00001000",2))
    write8(int("00000001",2))
    write8(int("00000100",2))

    write8(int("00001111",2))
    write8(int("00000001",2))
    write8(int("00000110",2))

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
        if len(tmp) == 2:
            rs_val = int(tmp[0])
            try:
                value = int(tmp[1], 2)
                write8(value, rs_val, bits=8)
            except TypeError:
                value = ord(tmp[1])
                write8(value, rs_val, bits=BITS)
        elif len(tmp) == 3:
            rs_val = int(tmp[0])
            valu1 = int(tmp[1], 2)
            valu2 = int(tmp[2], 2)
            write4(valu1, rs_val)
            write4(valu2, rs_val)
        else:
            sys.stderr.write("Invalid format: X XXXXXXXX, X XXXX XXXX, or X a\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bits', '-b', type=int, default=4, help="use 4- or 8-bit interface (default: 4)")
    parser.add_argument('--delay', '-d', type=float, default=1e-3, help="delay (in sec) between successive clocks")
    parser.add_argument('--arbitrary', '-a', action='store_true', help="send arbitrary command sequences")
    parser.add_argument('message', type=str, default="hello world", nargs='?', help="string to display")
    args = parser.parse_args()
    if args.bits != 4 and args.bits != 8:
        raise Exception("--bits must be 4 or 8")
    else:
        BITS = args.bits
    DELAY = args.delay

    GPIO.setmode( GPIO.BCM )

    if BITS == 4:
        GPIO.setup([PIN_RS, PIN_EN] + PIN_D[4:8], GPIO.OUT, initial=GPIO.LOW )
    else:
        GPIO.setup([PIN_RS, PIN_EN] + PIN_D[0:8], GPIO.OUT, initial=GPIO.LOW )

    try:
        if args.arbitrary:
            prog_arbitrary()
        else:
            prog_printmsg(args.message)
    except:
        GPIO.cleanup()
        raise
    GPIO.cleanup()
