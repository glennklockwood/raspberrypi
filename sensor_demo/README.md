MCP3008 Sensor Demo
================================================================================

This directory contains a few scripts that demonstrate how to poll analog
sensors (a 10K thermistor and a photocell), convert raw readings into physical
values like voltages and temperatures, and upload those measurements to a
Google Sheets document using the Google API Python client.

These scripts use a simplified SPI interface that is designed to be
understandable, not extensible.
