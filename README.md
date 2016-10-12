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

mcp3008spi.py
--------------------------------------------------------------------------------
`mcp3008spi.py` is a Python script that interacts with the [MCP3008][]
eight-channel analog-to-digital converter chip.  It implements a very simple SPI
interface in Python and includes a function that sends basic data retrieval
commands to the MCP3008 via SPI.  The SPI functions contained in this script
are re-usable, but very simple.

poll\_sensors.py
--------------------------------------------------------------------------------
`poll_sensors.py` is a tool that uses `mcp3008spi.py` to poll two simple analog
sensors: a [10K thermistor][] and a [CdS photocell][].  It converts the reading
obtained from the thermistor into an actual temperature using interpolation of
the data in `temperatures.txt`, and it also can upload temperature readings to
a Google Sheets spreadsheet.

upload\_sensordata.py
--------------------------------------------------------------------------------
`upload_sensordata.py` is a crude script that uses the Google Sheets API to
upload a set of arguments (specified via `sys.argv`) to a given Google Sheets
document.  It will also update the range on a plot to include the newly uploaded
data so you can see sensor data updating in almost real time from anywhere that
can access your Google Sheet.

[physical computing]: https://www.raspberrypi.org/learning/physical-computing-guide/
[camera module]: https://www.raspberrypi.org/products/camera-module/
[MK152RS]: https://www.amazon.com/Spinning-LED-Wheel-KIT-MK152RS/dp/B00R4WVQXW
[CD4017BE]: https://store.ti.com/CD4017BE.aspx
[CD4017BE blog post]: https://glennklockwood.blogspot.com/2016/10/learning-electronics-with-roulette.html
[MCP3008]: https://www.adafruit.com/product/856
[10K thermistor]: https://www.adafruit.com/products/372
[CdS photocell]: https://www.adafruit.com/products/161
