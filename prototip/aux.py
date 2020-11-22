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

def open_valve(n):
	global valves_t0
	if(relays[n].value == 0):
		relays[n].on()
		valves_t0[n] = time()
		print("Obertura electrovàlvula", n, ".")

def close_valve(n):
	global valves_t1
	if(relays[n].value == 1):
		if(time()-valves_t0[n] < BOUNCE_TIME): # Mínim temps d'obertura de la vàlvula
			sleep(BOUNCE_TIME-(time()-valves_t0[n])) # Esperem el temps que falta per tancar
		relays[n].off()
		valves_t1[n] = time()
		print("Tancament electrovàlvula", n, ". Reg:", round((valves_t1[n]-valves_t0[n])*FLOW, 1), "ml\n")

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

	for i in range(SYS_SIZE):
			soil_sensors_vcc[i].on()
		
#		if (soil_sensors[0].value == DRY):
#			threading.Thread(target=irrigate, args=(buttons[0],)).start()
#			
#		if (soil_sensors[1].value == DRY):
#			threading.Thread(target=irrigate, args=(buttons[1],)).start()

	for i in range(SYS_SIZE):
		print("Humitat test", i, ":", soil_sensors[i].value)
	
	
	sleep(POLL_TIME)
			
	for i in range(SYS_SIZE):
		soil_sensors_vcc[i].off()

poll_temp_sensor():
	
	try:
			print("Temperatura (ºC): ", temp_sensor.temperature)
		except RuntimeError:
			print("RuntimeError, try again ...")
			poll_temp_sensor()
			continue

def irrigate(btn):

	print("\nAuto irrigation\n")
	open_valve(btn)
	sleep(IRRIGATION_TIME)
	close_valve(btn)
	sys.exit(0) # Matem el thread

def post():


	payload = {'date': time(), 'moisture': [0, 1]}

	r = requests.post(url, data=json.dumps(payload))
	print(r.status_code, r.text)