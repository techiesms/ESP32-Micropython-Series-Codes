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
<h3> LED1 </h3>
<button name="LED1" value='ON' type='submit'>  ON </button>
<button name="LED1" value='OFF' type='submit'> OFF </button>
<h3> LED2 </h3>
<button name="LED2" value='ON' type='submit'>  ON </button>
<button name="LED2" value='OFF' type='submit'> OFF </button>
<h3> LED3 </h3>
<button name="LED3" value='ON' type='submit'>  ON </button>
<button name="LED3" value='OFF' type='submit'> OFF </button>
<h3> LED4 </h3>
<button name="LED4" value='ON' type='submit'>  ON </button>
<button name="LED4" value='OFF' type='submit'> OFF </button>
</center>
'''

# Output Pin Declaration 
LED1 = machine.Pin(15,machine.Pin.OUT)
LED1.value(0)

LED2 = machine.Pin(2,machine.Pin.OUT)
LED2.value(0)

LED3 = machine.Pin(4,machine.Pin.OUT)
LED3.value(0)

LED4 = machine.Pin(22,machine.Pin.OUT)
LED4.value(0)

# Initialising Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

Host = '' # Empty means, it will allow all IP address to connect
Port = 80 # HTTP port
s.bind(('',80)) # Host,Port

s.listen(5) # It will handle maximum 5 clients at a time

# main loop
while True:
  connection_socket,address=s.accept() # Storing Conn_socket & address of new client connected
  print("Got a connection from ", address)
  request=connection_socket.recv(1024) # Storing Response coming from client
  print("Content ", request) # Printing Response 
  request=str(request) # Coverting Bytes to String
  # Comparing & Finding Postion of word in String 
  LED1_ON =request.find('/?LED1=ON')
  LED1_OFF =request.find('/?LED1=OFF')
  
  LED2_ON =request.find('/?LED2=ON')
  LED2_OFF =request.find('/?LED2=OFF')
  
  LED3_ON =request.find('/?LED3=ON')
  LED3_OFF =request.find('/?LED3=OFF')
  
  LED4_ON =request.find('/?LED4=ON')
  LED4_OFF =request.find('/?LED4=OFF')
  
  if(LED1_ON==6):
    LED1.value(1)   
  if(LED1_OFF==6):
    LED1.value(0)
    
  if(LED2_ON==6):
    LED2.value(1)   
  if(LED2_OFF==6):
    LED2.value(0)
    
  if(LED3_ON==6):
    LED3.value(1)   
  if(LED3_OFF==6):
    LED3.value(0)
    
  if(LED4_ON==6):
    LED4.value(1)   
  if(LED4_OFF==6):
    LED4.value(0)
    
  # Sending HTML document in response everytime to all connected clients  
  response=html 
  connection_socket.send(response)
  
  #Closing the socket
  connection_socket.close() 

