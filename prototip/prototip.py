#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause
import threading
import requests
import json

import gpiozero

# Definició de constants
POLL_FREQUENCY = 5
POLL_TIME = 0.25
IRRIGATION_TIME = 1

DRY = 0
WET = 1

url = 'http://192.168.1.134:8080'
payload = {'date': time(), 'moisture': [0, 1]}

# Situació dels pins per a cada component
RELAY_1 = "BOARD11"
RELAY_2 = "BOARD12"

BUTTON_1 = "BOARD16"
BUTTON_2 = "BOARD18"

SENSOR1 = "BOARD31"
SENSOR2 = "BOARD35"
SENSOR1_VCC = "BOARD29"
SENSOR2_VCC = "BOARD33"

# Creació dels objectes.
relay1 = gpiozero.OutputDevice(RELAY_1, active_high=False, initial_value=False)
relay2 = gpiozero.OutputDevice(RELAY_2, active_high=False, initial_value=False)

button1 = gpiozero.Button(BUTTON_1)
button2 = gpiozero.Button(BUTTON_2)

valve1_t0 = 0
valve1_t1 = 0
valve2_t0 = 0
valve2_t1 = 0

sensor1 = gpiozero.DigitalInputDevice(SENSOR1, pull_up=None, active_state=False)
sensor2 = gpiozero.DigitalInputDevice(SENSOR2, pull_up=None, active_state=False)
sensor1_vcc = gpiozero.OutputDevice(SENSOR1_VCC, active_high=True, initial_value=False)
sensor2_vcc = gpiozero.OutputDevice(SENSOR2_VCC, active_high=True, initial_value=False)


# Definició de funcions.
def open_valve(btn):
	global valve1_t0, valve2_t0
	if(btn == button1 and relay1.value == 0):
		relay1.on()
		valve1_t0 = time()
		print("Electrovàlvula 1: Obertura.")
	if(btn == button2 and relay2.value == 0):
		relay2.on()
		valve2_t0 = time()
		print("Electrovàlvula 2: Obertura.")
		
def close_valve(btn):
	global valve1_t1, valve2_t1
	if(btn == button1 and relay1.value == 1):
		relay1.off()
		valve1_t1 = time()
		print("Electrovàlvula 1: Tancament. Temps de reg: ", round(valve1_t1-valve1_t0, 1), " segons\n")
	if(btn == button2 and relay2.value == 1):
		relay2.off()
		valve2_t1 = time()
		print("Electrovàlvula 2: Tancament. Temps de reg: ", round(valve2_t1-valve2_t0, 1), " segons\n")

def set_valves(status):
	if status:
		open_valve(button1)
		open_valve(button2)
	else:
		close_valve(button1)
		close_valve(button2)
		
def poll_sensors():
	while 1:
		sensor1_vcc.on()
		sensor2_vcc.on()
		
		if (sensor1.value == DRY):
			threading.Thread(target=irrigate, args=(button1,)).start()
			
		if (sensor2.value == DRY):
			threading.Thread(target=irrigate, args=(button2,)).start()
		
		sleep(POLL_TIME)
				
		sensor1_vcc.off()
		sensor2_vcc.off()

		post()
		
		sleep(POLL_FREQUENCY)
	
def irrigate(btn):
	print("\nAuto irrigation\n")
	open_valve(btn)
	sleep(IRRIGATION_TIME)
	close_valve(btn)
	sys.exit(0) # Matem el thread
		
def init():

	print(time())
	print(ctime())
	
	# Tanquem les dues electrovàlvules
	set_valves(False)

	button1.when_pressed = open_valve
	button1.when_released = close_valve

	button2.when_pressed = open_valve
	button2.when_released = close_valve

def post():
	r = requests.post(url, data=json.dumps(payload))
	print(r.status_code, r.text)

def main_loop():

	init()
	poll_sensors()

if __name__ == "__main__":
	try:
		main_loop()
	except KeyboardInterrupt:
		print("\n")
		# Tanquem les dues electrovàlvules
		set_valves(False)
		print("\nSortida de l'aplicació\n")
		sys.exit(0)
