import machine
import usocket as socket
import time
import network


timeout = 0 # WiFi Connection Timeout variable 

wifi = network.WLAN(network.STA_IF)

# Restarting WiFi
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

wifi.connect('SmS_jiofi','sms123458956')

if not wifi.isconnected():
    print('connecting..')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(1)
        
if(wifi.isconnected()):
    print('Connected...')
    print('network config:', wifi.ifconfig())
    
# HTML Document

html='''<!DOCTYPE html>
<html>
<center><h2>ESP32 Webserver </h2></center>
<form>
<center>
<h3> LED </h3>
<button name="LED" value='ON' type='submit'>  ON </button>
<button name="LED" value='OFF' type='submit'> OFF </button>
</center>
'''

# Output Pin Declaration 
LED = machine.Pin(2,machine.Pin.OUT)
LED.value(0)

# Initialising Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

Host = '' # Empty means, it will allow all IP address to connect
Port = 80 # HTTP port
s.bind((Host,Port)) # Host,Port

s.listen(5) # It will handle maximum 5 clients at a time

# main loop
while True:
  connection_socket,address=s.accept() # Storing Conn_socket & address of new client connected
  print("Got a connection from ", address)
  request=connection_socket.recv(1024) # Storing Response coming from client
  print("Content ", request) # Printing Response 
  request=str(request) # Coverting Bytes to String
  # Comparing & Finding Postion of word in String 
  LED_ON =request.find('/?LED=ON')
  LED_OFF =request.find('/?LED=OFF')
  
  if(LED_ON==6):
    LED.value(1)
    
  if(LED_OFF==6):
    LED.value(0)
    
  # Sending HTML document in response everytime to all connected clients  
  response=html 
  connection_socket.send(response)
  
  #Closing the socket
  connection_socket.close() 