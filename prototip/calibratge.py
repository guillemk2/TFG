import sys
from time import time, sleep
import gpiozero
from MCP3008 import MCP3008

DRY_VALUE = 980			# Valor analògic per a un entorn d'humitat 0%
WET_VALUE = 230			# Valor analògic per a un entorn d'humitat 100%

analog_moisture_sensors = MCP3008()

def value_to_percent(v):
	if (v < WET_VALUE):
		v = WET_VALUE
	if (v > DRY_VALUE):
		v = DRY_VALUE

	return round((1-(v-WET_VALUE)/(DRY_VALUE-WET_VALUE))*100, 0)

if __name__ == "__main__":

	sensor_vcc = gpiozero.OutputDevice("BOARD29", active_high=True, initial_value=False)
	sensor_vcc.on()

	start_time = time()
	print("Start:", start_time)

	while True:

		print("+", round(time()-start_time, 5), "ms", value_to_percent(analog_moisture_sensors.read(channel = 5)), "%")
		sleep(0.25)
