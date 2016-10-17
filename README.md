Raspberry Pi
================================================================================
These are various scripts and programs that I have been making as I play with
[physical computing][] on my Raspberry Pi using its GPIO and the
[camera module][].  Most of these scripts are just demonstrations of basic
functionality creating for my own edification, but maybe someone else will find
them useful in their adventures.

cd4017be.py
--------------------------------------------------------------------------------
`cd4017be.py` is a Python implementation of the [CD4017BE][] counter/divider IC.
I created it as a replacement for the physical CD4017BE that came with a
[Spinning LED Wheel Kit][MK152RS] with which I've been playing.  I've documented
this script and the associated LED kit on my [blog][CD4017BE blog post].

spi
--------------------------------------------------------------------------------
This is a Python package that provides a simple software interface for SPI
devices.  I've also created some subclasses for specific SPI devices with which
I've played; for example, `poll_mcp3008.py` is a script that uses the 
`spi.MCP3008` class to get measurements from MCP3008 analog-digital converter
chips.

[physical computing]: https://www.raspberrypi.org/learning/physical-computing-guide/
[camera module]: https://www.raspberrypi.org/products/camera-module/
[MK152RS]: https://www.amazon.com/Spinning-LED-Wheel-KIT-MK152RS/dp/B00R4WVQXW
[CD4017BE]: https://store.ti.com/CD4017BE.aspx
[CD4017BE blog post]: https://glennklockwood.blogspot.com/2016/10/learning-electronics-with-roulette.html
