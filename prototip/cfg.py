#!/usr/bin/env python3

from time import time
import numpy as np
import gpiozero

# CONSTANTS

# Duració dels events
POLL_FREQUENCY = 5
POLL_TIME = 0.25
IRRIGATION_TIME = 1

# Valors d'humitat
DRY = 0
WET = 1

# Paràmetres de connexió al servidor
url = 'http://192.168.1.134:8080'
payload = {'date': time(), 'moisture': [0, 1]}

# Situació dels pins per a cada component
RELAY_0 = "BOARD11"
RELAY_1 = "BOARD12"

BUTTON_0 = "BOARD16"
BUTTON_1 = "BOARD18"

SENSOR0 = "BOARD31"
SENSOR1 = "BOARD35"
SENSOR0_VCC = "BOARD29"
SENSOR1_VCC = "BOARD33"

# Creació dels OBJECTES.
relays = []
relays.append(gpiozero.OutputDevice(RELAY_0, active_high=False, initial_value=False))
relays.append(gpiozero.OutputDevice(RELAY_1, active_high=False, initial_value=False))
relays = np.array(relays)

print(relays.size)
print(relays)

print("Valor del relé 0: ", relays[0].value)
print(relays[1].value)

buttons[0] = gpiozero.Button(BUTTON_0)
buttons[1] = gpiozero.Button(BUTTON_1)

sensors[0] = gpiozero.DigitalInputDevice(SENSOR0, pull_up=None, active_state=False)
sensors[1] = gpiozero.DigitalInputDevice(SENSOR1, pull_up=None, active_state=False)
sensors_vcc[0] = gpiozero.OutputDevice(SENSOR0_VCC, active_high=True, initial_value=False)
sensors_vcc[1] = gpiozero.OutputDevice(SENSOR1_VCC, active_high=True, initial_value=False)

# Variables GLOBALS
valves_t0[0] = 0 # Darrer instant que la vàlvula 0 ha estat oberta.
valves_t1[0] = 0 # Darrer instant que la vàlvula 0 ha estat tancada.
valves_t0[1] = 0 # Darrer instant que la vàlvula 1 ha estat oberta.
valves_t1[1] = 0 # Darrer instant que la vàlvula 1 ha estat tancada.