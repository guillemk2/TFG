#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause
import threading
import requests
import json
import gpiozero
import adafruit_dht
from numpyencoder import NumpyEncoder

# Constants
from cfg import SYS_SIZE, POLL_FREQUENCY, POLL_TIME, IRRIGATION_TIME, BOUNCE_TIME, FLOW, DRY, WET, url, headers
# Objectes
from cfg import temp_sensor,relays, buttons, soil_sensors, soil_sensors_vcc
# Variables globals
from cfg import temperature, moisture, irrigation, valves_t0, valves_t1

# Definició de funcions.
		
def init():

	print("Posada en marxa del sistema: ", ctime(), "\n")
	
	# Tanquem les dues electrovàlvules
	set_valves(False)

	# Assignem accions per a les interrupcions de polsació dels botons
	for i in range(SYS_SIZE):
		buttons[i].when_pressed = button_pressed
		buttons[i].when_released = button_released

def open_valve(n):
	
	if(relays[n].value == 0):
		relays[n].on()
		valves_t0[n] = time()
		#print("Obertura electrovàlvula", n, ".")

def close_valve(n):
	
	if(relays[n].value == 1):
		if(time()-valves_t0[n] < BOUNCE_TIME): # Mínim temps d'obertura de la vàlvula
			sleep(BOUNCE_TIME-(time()-valves_t0[n])) # Esperem el temps que falta per tancar
		relays[n].off()
		valves_t1[n] = time()
		volume = (valves_t1[n]-valves_t0[n])*FLOW
		irrigation[n] += volume
		print("Test", n, ". Reg:", round(volume, 1), "ml. Reg acumulat des del darrer cicle", round(irrigation[n], 1), "ml")

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
		moisture[i] = soil_sensors[i].value

		if (moisture[i] == DRY):
			threading.Thread(target=irrigate, args=(i,)).start()

	sleep(POLL_TIME)
			
	for i in range(SYS_SIZE):
		soil_sensors_vcc[i].off()

def poll_temp_sensor():
	global temperature
	try:
		temperature = temp_sensor.temperature
		print("Temperatura:", temperature, "ºC")
	except RuntimeError:
		print("RuntimeError, try again ...")
		poll_temp_sensor()

def irrigate(n):
	open_valve(n)
	sleep(IRRIGATION_TIME)
	close_valve(n)
	sys.exit(0) # Matem el thread

def post():

	# Convermim el timestamp a milisegons per a la correcta lectura per MongoDB
	payload = {'date': time()*1000, 'temperature': temperature}

	plants = []
	for i in range(SYS_SIZE):
		plants.append({'moisture': moisture[i], 'irrigation': round(irrigation[i], 1)})
		irrigation[i] = 0 # Restablim quantitat de reg acumulada
	payload["plants"] = plants

	try:
		r = requests.post(url, headers=headers, data=json.dumps(payload, cls=NumpyEncoder))
		print("Dades enviades a ", ctime(), ", codi resposta: ", r.status_code, "\n")
	except ConnectionRefusedError, ConnectionError:
		print("Connexió amb servidor fallida a ", ctime())
	