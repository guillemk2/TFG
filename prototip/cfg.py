#!/usr/bin/env python3

from time import time
import numpy as np
import gpiozero
import adafruit_dht

# CONSTANTS

# Número de testos (mida del sistema)
SYS_SIZE = 2

# Duració dels events (en segons)
POLL_FREQUENCY = 5 		# Freqüència de lectura dels sensors
POLL_TIME = 0.25		# Duració de la lectura dels sensors
IRRIGATION_TIME = 1		# Temps de reg
BOUNCE_TIME = 0.25		# Temps de rebot dels botons (mínim temps de reg)

# Valors d'humitat
DRY = 0  # Sec
WET = 1  # Humit

# Paràmetres de connexió al servidor
url = 'http://192.168.1.134:8080'
payload = {'date': time(), 'moisture': [0, 1]}

# Situació dels pins per a components únics.
TEMP_SENSOR_PIN = 22 # Pin 15: GPIO22

# Situació dels pins per a components múltiples.
RELAY_PINS = []
BUTTON_PINS = []
SOIL_SENSOR_PINS = []
SOIL_SENSOR_VCC_PINS = []

RELAY_PINS.append("BOARD11") # Relé 0
RELAY_PINS.append("BOARD12") # Relé 1

BUTTON_PINS.append("BOARD16") # Botó 0
BUTTON_PINS.append("BOARD18") # Botó 1

SOIL_SENSOR_PINS.append("BOARD31") # Sensor d'humitat del sòl 0
SOIL_SENSOR_PINS.append("BOARD35") # Sensor d'humitat del sòl 1

SOIL_SENSOR_VCC_PINS.append("BOARD29") # Alimentació del sensor d'humitat del sòl 0
SOIL_SENSOR_VCC_PINS.append("BOARD33") # Alimentació del sensor d'humitat del sòl 1

RELAY_PINS = np.array(RELAY_PINS)
BUTTON_PINS = np.array(BUTTON_PINS)
SOIL_SENSOR_PINS = np.array(SOIL_SENSOR_PINS)
SOIL_SENSOR_VCC_PINS = np.array(SOIL_SENSOR_VCC_PINS)


# Creació dels OBJECTES únics.
temp_sensor = adafruit_dht.DHT22(TEMP_SENSOR_PIN)

# Creació dels OBJECTES múltiples.
relays = []
buttons = []
soil_sensors = []
soil_sensors_vcc = []

for i in range(SYS_SIZE):
	relays.append(gpiozero.OutputDevice(RELAY_PINS[i], active_high=False, initial_value=False))
	buttons.append(gpiozero.Button(BUTTON_PINS[i]))
	soil_sensors.append(gpiozero.DigitalInputDevice(SOIL_SENSOR_PINS[i], pull_up=None, active_state=False))
	soil_sensors_vcc.append(gpiozero.OutputDevice(SOIL_SENSOR_VCC_PINS[i], active_high=True, initial_value=False))

relays = np.array(relays)
buttons = np.array(buttons)
soil_sensors = np.array(soil_sensors)
soil_sensors_vcc = np.array(soil_sensors_vcc)


# Variables GLOBALS
valves_t0 = []
valves_t1 = []

for i in range(SYS_SIZE):
	valves_t0.append(time()) # Darrer instant que les vàlvules han estat obertes
	valves_t1.append(time()) # Darrer instant que les vàlvules han estat tancades

valves_t0 = np.array(valves_t0,)
valves_t1 = np.array(valves_t1,)

