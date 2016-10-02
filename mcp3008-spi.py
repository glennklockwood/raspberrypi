#!/usr/bin/env python
#
#  A script to play around with the bitwise operators necessary to communicate
#  with the MCP3008 ADC using software-implemented SPI.
#
# The MCP3008 protocol is described as:
#
# 1. The first clock received with CS low and DIN high will constitute a start
#    bit.
# 2. The SGL/DIFF bit follows the start bit and will determine if the
#    conversion will be done using single-ended or differential input mode
# 3. The next three bits (D0, D1 and D2) are used to select the input channel
#    configuration.
# 4. The device will begin to sample the analog input on the fourth rising
#    edge of the clock after the start bit has been received.
# 5. The sample period will end on the falling edge of the fifth clock
#    following the start bit.
# 6. Once the D0 bit is input, one more clock is required to complete the
#    sample and hold period (DIN is a "don't care" for this clock).
# 7. On the falling edge of the next clock, the device will output a low null
#    bit.
# 8. The next 10 clocks will output the result of the conversion with MSB first
#
import sys

if len(sys.argv) < 2:
    channel = 0
else:
    channel = int(sys.argv[1])

print "Selecting channel %d" % channel

commandout = channel
print "Command: {0:b}".format(commandout)

### 0x18 gives us five bits, 11000
### |= 0x18 combines the 11000 with our channel id
commandout |= 0x18 # OR
print "Command: {0:b}".format(commandout)

commandout <<= 3 # shift off three bits on left
print "Command: {0:b}".format(commandout)

print "Sending five bits now"
cmd = ""
for i in range(5):
    # 0x80 gives us 10000000, which always checks the MSB
    if commandout & 0x80:
        cmd += "1"
    else:
        cmd += "0"
    # shift off the MSB
    commandout <<= 1

print "Sent [%s]" % cmd
