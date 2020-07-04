/* 
 * Manipulating the GPIO controller on BCM2835
 *
 * register 00: r0 +  0 = GPFSEL0 = GPIO Function Select 0 = for pins 0-9
 * register 01: r0 +  4 = GPFSEL1 = GPIO Function Select 1 = for pins 10-19
 * register 02: r0 +  8 = GPFSEL2 = GPIO Function Select 2 = for pins 20-29
 * register 03: r0 + 12 = GPFSEL3 = GPIO Function Select 3 = for pins 30-39
 * register 04: r0 + 16 = GPFSEL4 = GPIO Function Select 4 = for pins 40-49
 * register 05: r0 + 20 = GPFSEL5 = GPIO Function Select 5 = for pins 50-54
 * register 06: r0 + 24 = reserved
 * register 07: r0 + 28 = GPSET0 = GPIO Pin Output Set 0 = for pins 0-31
 * register 08: r0 + 32 = GPSET1 = GPIO Pin Output Set 1 = for pins 32-54
 * register 09: r0 + 36 = reserved
 * register 10: r0 + 40 = GPCLR0 = GPIO Pin Output Clear 0 = for pins 0-31
 * register 11: r0 + 44 = GPCLR1 = GPIO Pin Output Clear 1 = for pins 32-54
 * register 12: r0 + 48 = reserved
 * register 13: r0 + 52 = GPLEV0
 * register 14: r0 + 56 = GPLEV1
 * register 15: r0 + 60 = reserved
 * register 16: r0 + 64 = GPEDS0
 * register 17: r0 + 68 = GPEDS1
 * register 18: r0 + 72 = reserved
 * register 19: r0 + 76 = GPREN0
 * register 20: r0 + 80 = GPREN1
 * register 21: r0 + 84 = reserved
 * register 22: r0 + 88 = GPFEN0
 * register 23: r0 + 92 = GPFEN1
 * register 24: r0 + 96 = reserved
 * register 25: r0 + 100 = GPHEN0
 * register 26: r0 + 104 = GPHEN1
 * register 27: r0 + 108 = reserved
 * register 28: r0 + 112 = GPLEN0
 * register 29: r0 + 116 = GPLEN1
 * register 30: r0 + 120 = reserved
 * register 31: r0 + 124 = GPAREN0
 * register 32: r0 + 128 = GPAREN1
 * register 33: r0 + 132 = reserved
 * register 34: r0 + 136 = GPAFEN0
 * register 35: r0 + 140 = GPAFEN1
 * register 36: r0 + 144 = reserved
 * register 37: r0 + 148 = GPPUD
 * register 38: r0 + 152 = GPPUDCLK0
 * register 39: r0 + 156 = GPPUDCLK1
 * register 40: r0 + 160 = reserved
 * register 41: r0 + 164 = test
 *
 */
.section .init
.globl _start
_start:

/* Store 0x20200000 in r0; this is the base address of the GPIO controller */
ldr r0, =0x20200000

/*
 * Enable output to GPIO pin 47 (the ACT LED) by flipping a bit in a specific
 * register in the GPIO controller.
 */
mov r1, #1  /* r1 = 00000000 00000000 00000000 00000001 */

lsl r1, #21 /* r1 = 00000000 00100000 00000000 00000000 */

str r1, [r0, #16]  /* write contents of r1 into address given by r0 + 16 (GPFSEL4) */

/*
 * So writing r1 to (r0 + 16) results in
 *
 * r0 + 16 = pins 40-49     00000000 00100000 00000000 00000000
 *
 * Bear in mind that for GPFSEL[0-5] registers, the mapping of bits within each
 * 32-bit register to the 10 GPIO pins for which it is responsible is
 *
 *                          MSB                             LSB
 *                          xx999888 77766655 54443332 22111000
 *
 * So writing 00000000 00100000 00000000 00000000 to (r0 + 16) writes the `001`
 * command code into the three-bit range reserved for the 7th GPIO in pins 40-49
 * (i.e., pin #47):
 *
 *                          xx999888 77766655 54443332 22111000
 * r0 + 16 = pins 40-49     00000000 00100000 00000000 00000000
 *
 * From the command table, 000 = GPIO pin is an input
 *                         001 = GPIO pin is an output 
 *                         100 = GPIO pin takes alt function 0
 *                         101 = GPIO pin takes alt function 1
 *                         110 = GPIO pin takes alt function 2
 *                         111 = GPIO pin takes alt function 3
 *                         011 = GPIO pin takes alt function 4
 *                         010 = GPIO pin takes alt function 5
 *
 * Thus we are setting pin #47 to command code 001 ("is an output")
 */

/*
 * Turn off GPIO pin 47
 *
 * We do this by flipping the 15th bit (for the 32+15th pin) in the
 * "GPIO Pin Output Clear 1" register in the GPIO controller
 */
mov r1, #1  /* 00000000 00000000 00000000 00000001 */

lsl r1, #15 /* 00000000 00000000 10000000 00000000 */

str r1, [r0, #32] /* write contents of r1 into address given by r0 + 32 */

/*
 * Loop forever
 */
loop$:
b loop$
