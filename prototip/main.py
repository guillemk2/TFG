#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause, signal, SIGTERM
import threading
import requests
import json
import gpiozero
import adafruit_dht

# Constants
from cfg import SYS_SIZE, POLL_FREQUENCY, POLL_TIME, IRRIGATION_TIME, BOUNCE_TIME, FLOW, DRY, WET, url, headers
# Objectes
from cfg import temp_sensor,relays, buttons, soil_sensors, soil_sensors_vcc, f
# Variables globals
from cfg import temperature, moisture, irrigation, valves_t0, valves_t1

# Funcions auxiliars
from aux import init, poll_soil_sensors, poll_temp_sensor, post, set_valves

def main_loop():

	while 1:
		
		poll_soil_sensors()

		poll_temp_sensor()

		post()
		
		sleep(POLL_FREQUENCY)

if __name__ == "__main__":

	init()
	main_loop()