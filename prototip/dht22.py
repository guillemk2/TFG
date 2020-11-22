import adafruit_dht
import time
import board

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Office"

MINUTES_BETWEEN_READS = 10
METRIC_UNITS = True
# ---------------------------------

dhtSensor = adafruit_dht.DHT22("GPIO22")

while True:
        try:
                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

        except RuntimeError:
                print("RuntimeError, trying again...")
                continue
                
        
        print(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
        
        humidity = format(humidity,".2f")

        print(SENSOR_LOCATION_NAME + " Humidity(%)", humidity)

        time.sleep(MINUTES_BETWEEN_READS)