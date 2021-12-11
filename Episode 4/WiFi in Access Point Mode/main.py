import network

wifi = network.WLAN(network.AP_IF)

wifi.active(True)
wifi.config(essid='ESP',authmode=network.AUTH_WPA_WPA2_PSK, password='password')
print(wifi.ifconfig())