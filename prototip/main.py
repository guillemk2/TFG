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

# Funcions auxiliars
import aux

def main_loop():

	aux.init()
	#aux.poll_sensors()

if __name__ == "__main__":
	try:
		main_loop()
	except KeyboardInterrupt:
		print("\n")
		# Tanquem les dues electrovàlvules
		set_valves(False)
		print("\nSortida de l'aplicació\n")
		sys.exit(0)
