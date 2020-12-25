#!/usr/bin/env python3

from time import time
import numpy as np
import gpiozero
import adafruit_dht
from MCP3008 import MCP3008

# CONSTANTS

# Número de testos (mida del sistema)
SYS_SIZE = 2

# Duració dels events (en segons)
POLL_FREQUENCY = 15*60	# Freqüència de lectura dels sensors (30 minuts)
POLL_TIME = 0.75		# Duració de la lectura dels sensors
IRRIGATION_TIME = 2		# Temps de reg
BOUNCE_TIME = 0.25		# Temps de rebot dels botons (mínim temps de reg)
FLOW = 1.65				# Cabal de les vàlvules en ml/s
DRY_VALUE = 980			# Valor analògic per a un entorn d'humitat 0%
WET_VALUE = 230			# Valor analògic per a un entorn d'humitat 100%
MOISTURE_THRESHOLD = 50	# Llindar d'humitat per aplicar el reg (%)

# Valors d'humitat
DRY = 0  # Sec
WET = 1  # Humit

# Paràmetres de connexió al servidor
url = 'http://127.0.0.1:8080'
headers = {'Content-Type': 'application/json'}

# Fitxer de logs
f = open("/home/pi/Documents/logs.txt", "a+")

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
analog_moisture_sensors = MCP3008()

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
temperature = 0.00

moisture = []
irrigation = []
valves_t0 = []
valves_t1 = []

for i in range(SYS_SIZE):
	moisture.append(0)
	irrigation.append(0.0)
	valves_t0.append(time()) # Darrer instant que les vàlvules han estat obertes
	valves_t1.append(time()) # Darrer instant que les vàlvules han estat tancades

valves_t0 = np.array(valves_t0,)
valves_t1 = np.array(valves_t1,)
moisture = np.array(moisture)
irrigation = np.array(irrigation)

