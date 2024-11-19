# raspi-diagnostics

Diagnostic tool to monitor the Raspberry Pi CPU temperature and voltage under load. Logs the following information to a CSV file and, periodically, to the screen:
* Timestamp
* CPU Temperature (°C)
* CPU Clock Speed (MHz)
* EXT5V (V)
* CPU Throttled Status

Dependencies
---
* Python 3
	* `sudo apt install python 3`
* stress
	* `sudo apt install stress`

Usage
---
Run the script and specify the duration of the stress test in seconds. For example: `python3 ./benchmark.py 300`


Credits
---
Adapted from https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd