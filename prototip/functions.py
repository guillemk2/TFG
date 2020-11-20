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