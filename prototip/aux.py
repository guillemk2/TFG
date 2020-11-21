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
from cfg import relays, buttons, sensors, sensors_vcc
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
	if(relays[n].value == 0):
		relays[n].on()
		valves_t0[n] = time()
		print("Electrovàlvula ", n, ": Obertura.")

def close_valve(n):
	if(relays[n].value == 1):
		relays[n].off()
		valves_t1[n] = time()
		print("Electrovàlvula ", n, ": Tancament. Temps de reg: ", round(valves_t1[n]-valves_t0[n], 1), " segons\n")

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