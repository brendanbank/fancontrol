# 
# from machine import Pin
# Pin(23, mode=Pin.IN, pull=Pin.PULL_UP)
#
import time
import machine
led = machine.Pin(23, machine.Pin.OUT)

while True:
    led.on()
    time.sleep(0.05)
    led.off()
    time.sleep(0.05)