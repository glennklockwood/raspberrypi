MCP3008 Sensor Demo
================================================================================

This directory contains a few scripts that demonstrate how to poll analog
sensors (a 10K thermistor and a photocell), convert raw readings into physical
values like voltages and temperatures, and upload those measurements to a
Google Sheets document using the Google API Python client.

These scripts use a simplified SPI interface that is designed to be
understandable, not extensible.

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

[MCP3008]: https://www.adafruit.com/product/856
[10K thermistor]: https://www.adafruit.com/products/372
[CdS photocell]: https://www.adafruit.com/products/161
