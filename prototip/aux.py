#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause
import threading
import requests
import json
import gpiozero

# Constants
from cfg import POLL_FREQUENCY, POLL_TIME, IRRIGATION_TIME, DRY, WET, url, payload
# Objectes
from cfg import relays, buttons, sensors, sensors_vcc
# Variables globals
from cfg import valves_t0, valves_t1

# Definició de funcions.
		
def init():

	print(time())
	print(ctime())
	
	# Tanquem les dues electrovàlvules
	set_valves(False)

	buttons[0].when_pressed = open_valve1
	buttons[0].when_released = close_valve1

	buttons[1].when_pressed = open_valve2
	buttons[1].when_released = close_valve2
	pause()

def open_valve1():

	if(relays[0].value == 0):
		relays[0].on()
		valves_t0[0] = time()
		print("Electrovàlvula 1: Obertura.")

def open_valve2():

	if(relays[1].value == 0):
		relays[1].on()
		valves_t0[1] = time()
		print("Electrovàlvula 2: Obertura.")
		
def close_valve2():
	
	if(relays[0].value == 1):
		relays[0].off()
		valves_t1[0] = time()
		print("Electrovàlvula 1: Tancament. Temps de reg: ", round(valves_t1[0]-valves_t0[0], 1), " segons\n")
	
def close_valve2():

	if(relays[1].value == 1):
		relays[1].off()
		valves_t1[1] = time()
		print("Electrovàlvula 2: Tancament. Temps de reg: ", round(valves_t1[1]-valves_t0[1], 1), " segons\n")

def set_valves(status):

	if status:
		open_valve1()
		open_valve2()
	else:
		close_valve1()
		close_valve2()
		
def poll_sensors():

	while 1:
		sensors_vcc[0].on()
		sensors_vcc[1].on()
		
		if (sensors[0].value == DRY):
			threading.Thread(target=irrigate, args=(buttons[0],)).start()
			
		if (sensors[1].value == DRY):
			threading.Thread(target=irrigate, args=(buttons[1],)).start()
		
		sleep(POLL_TIME)
				
		sensors_vcc[0].off()
		sensors_vcc[1].off()

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