from machine import Pin, Timer
import network
import time
from umqtt.robust import MQTTClient
import sys
import dht

sensor = dht.DHT11(Pin(4))                  # DHT11 Sensor on Pin 4 of ESP32

WIFI_SSID     = 'SSID'
WIFI_PASSWORD = 'PASS'

mqtt_client_id      = bytes('client_'+'12321', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'USERNAME'
ADAFRUIT_IO_KEY     = 'AIOKEY'

TEMP_FEED_ID      = 'temp'
HUM_FEED_ID      = 'hum'

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('connected')
    else:
        print('not connected')
        sys.exit()
        

connect_wifi() # Connecting to WiFi Router 


client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

        
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format - techiesms/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format - techiesms/feeds/hum   


def sens_data(data):
    sensor.measure()                    # Measuring 
    temp = sensor.temperature()         # getting Temp
    hum = sensor.humidity()
    client.publish(temp_feed,    
                  bytes(str(temp), 'utf-8'),   # Publishing Temp feed to adafruit.io
                  qos=0)
    
    client.publish(hum_feed,    
                  bytes(str(hum), 'utf-8'),   # Publishing Hum feed to adafruit.io
                  qos=0)
    print("Temp - ", str(temp))
    print("Hum - " , str(hum))
    print('Msg sent')
    
    
    
timer = Timer(0)
timer.init(period=5000, mode=Timer.PERIODIC, callback = sens_data)


     




