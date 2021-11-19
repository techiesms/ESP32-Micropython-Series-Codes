from machine import Timer,Pin

timer = Timer(0)

led = Pin(2,Pin.OUT)

timer.init(period=1000, mode=Timer.PERIODIC, callback = lambda t: led.value(not led.value()))