#!/usr/bin/env python3

from time import time
import gpiozero

# Definició de constants
POLL_FREQUENCY = 5
POLL_TIME = 0.25
IRRIGATION_TIME = 1

# Valors d'humitat
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