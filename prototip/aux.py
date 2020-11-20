#!/usr/bin/env python3

import sys
from time import time, ctime, sleep
from signal import pause
import threading
import requests
import json
import gpiozero

# Configuració
import config

# Definició de funcions.
		
def init():

	print(time())
	print(ctime())
	
	# Tanquem les dues electrovàlvules
	set_valves(False)

	cfg.button1.when_pressed = open_valve
	cfg.button1.when_released = close_valve

	cfg.button2.when_pressed = open_valve
	cfg.button2.when_released = close_valve

	pause()

def open_valve(btn):

	if(btn == cfg.button1 and cfg.relay1.value == 0):
		cfg.relay1.on()
		cfg.valve1_t0 = time()
		print("Electrovàlvula 1: Obertura.")

	if(btn == cfg.button2 and cfg.relay2.value == 0):
		cfg.relay2.on()
		cfg.valve2_t0 = time()
		print("Electrovàlvula 2: Obertura.")
		
def close_valve(btn):
	
	if(btn == cfg.button1 and cfg.relay1.value == 1):
		cfg.relay1.off()
		cfg.valve1_t1 = time()
		print("Electrovàlvula 1: Tancament. Temps de reg: ", round(valve1_t1-valve1_t0, 1), " segons\n")
	if(btn == cfg.button2 and cfg.relay2.value == 1):
		cfg.relay2.off()
		cfg.valve2_t1 = time()
		print("Electrovàlvula 2: Tancament. Temps de reg: ", round(valve2_t1-valve2_t0, 1), " segons\n")

def set_valves(status):

	if status:
		open_valve(cfg.button1)
		open_valve(cfg.button2)
	else:
		close_valve(cfg.button1)
		close_valve(cfg.button2)
		
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

def post():

	r = requests.post(url, data=json.dumps(payload))
	print(r.status_code, r.text)