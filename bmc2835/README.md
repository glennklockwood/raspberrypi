# Bare metal programming of the BMC2835 SOC

This contains some assembly designed to run directly on the BMC2835 SOC on
Raspberry Pi.  It was inspired by the [Baking Pi OS Development][] course online.
Read that for more information on getting set up, prerequisites, etc.

## Prerequisites

    # apt install gcc-arm-none-eabi

## Building

    $ make

## Installing

    # mount /dev/sda1 /mnt
    # cp blink.img /mnt/kernel.img
    # umount /mnt

Assumes `/dev/sda1` is the SD card you will be using to load this image into the
BMC2835.

[Baking Pi OS Development]: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/os/ok01.html
