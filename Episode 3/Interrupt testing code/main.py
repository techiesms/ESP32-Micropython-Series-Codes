from machine import Timer,Pin

timer = Timer(0)

led = Pin(2,Pin.OUT)
but = Pin(0, Pin.IN)

def buttons_irq(pin):
    print('Triggered')
    
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

timer.init(period=1000, mode=Timer.PERIODIC, callback = lambda t: led.value(not led.value()))