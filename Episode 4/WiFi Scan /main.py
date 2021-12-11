import network

wireless = network.WLAN(network.STA_IF)
wireless.active(True)

networks = wireless.scan()

print(networks)