/* 
 * Blinking the ACT LED on a Raspberry Pi board
 *
 * GPIO controller registers:
 *
 * Number | Address | Name    | Description             | Domain
 * -------|---------|---------|-------------------------|----------------
 * 00     | r0 +  0 | GPFSEL0 | GPIO Function Select 0  | for pins 0-9
 * 01     | r0 +  4 | GPFSEL1 | GPIO Function Select 1  | for pins 10-19
 * 02     | r0 +  8 | GPFSEL2 | GPIO Function Select 2  | for pins 20-29
 * 03     | r0 + 12 | GPFSEL3 | GPIO Function Select 3  | for pins 30-39
 * 04     | r0 + 16 | GPFSEL4 | GPIO Function Select 4  | for pins 40-49
 * 05     | r0 + 20 | GPFSEL5 | GPIO Function Select 5  | for pins 50-54
 * 07     | r0 + 28 | GPSET0  | GPIO Pin Output Set 0   | for pins 0-31
 * 08     | r0 + 32 | GPSET1  | GPIO Pin Output Set 1   | for pins 32-54
 * 10     | r0 + 40 | GPCLR0  | GPIO Pin Output Clear 0 | for pins 0-31
 * 11     | r0 + 44 | GPCLR1  | GPIO Pin Output Clear 1 | for pins 32-54
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
 * Begin of infinite loop
 */
loop$:

/*
 * Turn off GPIO pin 47
 *
 * We do this by flipping the 15th bit (for the 32+15th pin) in the
 * "GPIO Pin Output Clear 1" register in the GPIO controller
 */
mov r1, #1  /* 00000000 00000000 00000000 00000001 */
lsl r1, #15 /* 00000000 00000000 10000000 00000000 */
str r1, [r0, #44] /* write contents of r1 into address given by r0 + 44 */

/*
 * Kill some time doing basic arithmetic
 */
mov r2, #0x3F0000
wait1$:
sub r2, #1
cmp r2, #0
bne wait1$

/*
 * Turn on GPIO pin 47
 *
 * We do this by flipping the 15th bit (for the 32+15th pin) in the
 * "GPIO Pin Output Set 1" register in the GPIO controller
 */
mov r1, #1  /* 00000000 00000000 00000000 00000001 */
lsl r1, #15 /* 00000000 00000000 10000000 00000000 */
str r1, [r0, #32] /* write contents of r1 into address given by r0 + 32 */

/*
 * Kill some time doing basic arithmetic
 */
mov r2, #0x3F0000
wait2$:
sub r2, #1
cmp r2, #0
bne wait2$

/*
 * Loop forever
 */
b loop$
