#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause
import threading
import requests
import json
import gpiozero
import adafruit_dht

# Constants
from cfg import SYS_SIZE, POLL_FREQUENCY, POLL_TIME, IRRIGATION_TIME, BOUNCE_TIME, FLOW, DRY, WET, url
# Objectes
from cfg import temp_sensor,relays, buttons, soil_sensors, soil_sensors_vcc
# Variables globals
from cfg import temperature, moisture, irrigation, valves_t0, valves_t1

# Funcions auxiliars
from aux import init, poll_soil_sensors, poll_temp_sensor, post

def main_loop():

	while 1:
		
		#aux.poll_soil_sensors()

		poll_temp_sensor()

		#aux.post()
		
		sleep(POLL_FREQUENCY)

if __name__ == "__main__":
	try:

		init()
		main_loop()

	except KeyboardInterrupt:

		print("\n")
		# Tanquem les dues electrovàlvules
		set_valves(False)
		print("\nSortida de l'aplicació\n")
		sys.exit(0)
