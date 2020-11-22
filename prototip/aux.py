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

# Definició de funcions.
		
def init():

	print(time())
	print(ctime())
	
	# Tanquem les dues electrovàlvules
	set_valves(False)

	for i in range(SYS_SIZE):
		buttons[i].when_pressed = button_pressed
		buttons[i].when_released = button_released

	pause()

def open_valve(n):
	global valves_t0
	if(relays[n].value == 0):
		relays[n].on()
		valves_t0[n] = time()
		print("Obertura electrovàlvula", n)
		print("valves_t0: ", valves_t0)
		print("valves_t1: ", valves_t1)

def close_valve(n):
	global valves_t1
	if(relays[n].value == 1):
		relays[n].off()
		valves_t1[n] = time()
		print("Tancament electrovàlvula", n, "Temps de reg:", valves_t1[n]-valves_t0[n], "segons\n")
		print("valves_t0: ", valves_t0)
		print("valves_t1: ", valves_t1)
		
def set_valves(status):
	if status:
		for i in range(SYS_SIZE):
			open_valve(i)
	else:
		for i in range(SYS_SIZE):
			close_valve(i)
		
def button_pressed(btn):
	for i in range(SYS_SIZE):
		if (buttons[i] == btn):
			open_valve(i)

def button_released(btn):
	for i in range(SYS_SIZE):
		if (buttons[i] == btn):
			close_valve(i)

def poll_soil_sensors():

	while 1:
		soil_sensors_vcc[0].on()
		soil_sensors_vcc[1].on()
		
		if (soil_sensors[0].value == DRY):
			threading.Thread(target=irrigate, args=(buttons[0],)).start()
			
		if (soil_sensors[1].value == DRY):
			threading.Thread(target=irrigate, args=(buttons[1],)).start()
		
		sleep(POLL_TIME)
				
		soil_sensors_vcc[0].off()
		soil_sensors_vcc[1].off()

		post()
		
		sleep(POLL_FREQUENCY)
	
def irrigate(btn):

	print("\nAuto irrigation\n")
	open_valve(btn)
	sleep(IRRIGATION_TIME)
	close_valve(btn)
	sys.exit(0) # Matem el thread

def post():

	r = requests.post(url, data=json.dumps(payload))
	print(r.status_code, r.text)