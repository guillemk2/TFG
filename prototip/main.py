#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause
import threading
import requests
import json
import gpiozero

# Constants
from cfg import SYS_SIZE, POLL_FREQUENCY, POLL_TIME, IRRIGATION_TIME, DRY, WET, url, payload
# Objectes
from cfg import relays, buttons, soil_sensors, soil_sensors_vcc
# Variables globals
from cfg import valves_t0, valves_t1

# Funcions auxiliars
import aux


if __name__ == "__main__":
	try:

		aux.init()
		#aux.poll_sensors()

	except KeyboardInterrupt:

		print("\n")
		# Tanquem les dues electrovàlvules
		aux.set_valves(False)
		print("\nSortida de l'aplicació\n")
		sys.exit(0)
