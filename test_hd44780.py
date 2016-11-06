#!/usr/bin/env python
"""
Script to demonstrate how to program an LCD display driven by a HD44780 display
controller.
"""

import RPi.GPIO as GPIO
import time
import sys
import argparse

# Use 4-bit or 8-bit interface to HD44780 chip.
BITS = 4

PIN_RS = 27
# PIN_RW = grounded; we will never read register states
PIN_EN = 22

# Define pins D0 through D7
PIN_D = [ 12, 16, 20, 21, 18, 23, 24, 25 ]

PIN_NAMES = {
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

DELAY = 1.0e-3 # in seconds

def clock( ):
    """
    Pulse the EN pin to tell the chip to read/write to pins d0-d7.  There are
    some timing requirements since commands generally take 37 microseconds to
    process.  If clock signals are sent faster than 37 microseconds apart
    (i.e., at about 27 kHz), commands will probably get corrupted or missed.

    In practice, a much longer delay is the safest way to proceed.  1 ms is a
    good number.
    """
    time.sleep(DELAY) # allow time for D0 - D7 to settle if recently changed
    GPIO.output(PIN_EN, GPIO.HIGH)
    time.sleep(DELAY) # allow time for edge to be detected
    GPIO.output(PIN_EN, GPIO.LOW)
    time.sleep(DELAY) # prevent D0 - D7 from being modified too quickly after a pulse

def write4( value, rs_val=GPIO.LOW ):
    """
    Write a 4-bit command.  Also handle the RS pin to dictate whether we are
    writing a command or a new display output.

    This is used during chip (re)initialization.
    """
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
        sys.stdout.write( "%2s=%1d " % (PIN_NAMES[PIN_D[i]], signal[i]))
    sys.stdout.write(" CLK\n")
    clock()

def write8( value, rs_val=GPIO.LOW, bits=None ):
    """
    Write an 8-bit command using either the 4-bit or 8-bit interface.  Also
    handle the RS pin to dictate whether we are writing a command or a new
    display output.
    """
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
        sys.stdout.write( "%2s=%1d " % (PIN_NAMES[PIN_D[i]], signal[i]))

    ### bits allows us to override the global 4/8-bit interface setting; this
    ### is necessary during initialization
    if bits is None:
        bits = BITS

    ### 4-bit interface requires an intermediate clock pulse to transit the
    ### four most significant bits
    if bits == 4:
        clock()
        GPIO.output( PIN_D[4:8], signal[0:4] )
        sys.stdout.write(" CLK\nrs=%d " % rs_val )
        for i in range(4,8):
            sys.stdout.write( "%2s=%1d " % (PIN_NAMES[PIN_D[i]], signal[i-4]))
    ### 8-bit interface just uses the remaining four pins
    else:
        GPIO.output( PIN_D[0:4], signal[0:4] )
        for i in range(0,4):
            sys.stdout.write( "%2s=%1d, " % (PIN_NAMES[PIN_D[i]], signal[i]))

    ### indicate that all parallel pins are ready to be consumed by the chip
    clock()
    sys.stdout.write(" CLK\n")

def prog_printmsg(msg):
    """
    Iniitialize display and print a user-provided message to it
    """
    ### initialization magic sequence - see figure 23/figure 24 in datasheet
    write4(int("0011", 2))
    write4(int("0011", 2))
    write4(int("0011", 2))
    if BITS == 4:
        write4(int("0010", 2))
        write8(int("00100000",2))
        func_display_cmd = int("00100000",2)
    else:
        write8(int("00110000",2))
        func_display_cmd = int("00110000",2)

    ### actually send the "function set" command to configure display dimensions
    write8(func_display_cmd | int("00001100",2))
    
    ### send the "display on/off control" command to power on the display (0x4)
    ### and enable cursor (0x2) + cursor blink (0x1)
    write8(int("00001111",2))

    ### send the "entry mode set" command to set left-to-right printing (0x2)
    write8(int("00000110",2))

    ### clear the display
    write8(int("00000001",2))

    ### write the message one character at a time
    for c in msg:
        write8(ord(c), GPIO.HIGH)

def prog_arbitrary():
    """
    Allow user to send arbitrary sequences to the device"
    """
    print "Input can be one of the following:"
    print "  X YYYY ZZZZ = RS=X, YYYY=d7-d4, clock, ZZZZ=d7-d4 (4-bit interface)"
    print "  X YYYYYYYY  = RS=X, YYYYYYYY=d7-d0 (8-bit interface)"
    print "  1 X         = RS=1, X is the character to print\n"
    print "Initialization sequence:"
    print "  0 00101000 (4-bit; repeat four times)"
    print "  0 00111000 (8-bit; repeat three times)"
    print "  0 00001111 (enable display, cursor, and blinking)"
    print "  0 00000110 (shift right after character is displayed)"
    print "  0 00000001 (clear display)"
    while True:
        try:
            new = raw_input("input> ")
        except (EOFError, KeyboardInterrupt):
            break
        tmp = new.split()
        if len(tmp) == 2:
            rs_val = int(tmp[0])
            try:
                value = int(tmp[1], 2)
                write8(value, rs_val, bits=8)
            except ValueError:
                value = ord(tmp[1])
                write8(value, rs_val, bits=BITS)
        elif len(tmp) == 3:
            rs_val = int(tmp[0])
            valu1 = int(tmp[1], 2)
            valu2 = int(tmp[2], 2)
            write4(valu1, rs_val)
            write4(valu2, rs_val)
        else:
            sys.stderr.write("Invalid format: X YYYYYYYY, X YYYY ZZZZ, or 1 X\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bits', '-b', type=int, default=4, help="use 4- or 8-bit interface (default: 4)")
    parser.add_argument('--delay', '-d', type=float, default=1e-3, help="delay (in sec) between successive clocks")
    parser.add_argument('--message', type=str, default=None, help="message to display")
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
        if args.message:
            prog_printmsg(args.message)
        else:
            prog_arbitrary()
    except:
        GPIO.cleanup()
        raise
    GPIO.cleanup()
