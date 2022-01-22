from machine import Pin
import time

#pin2绑定在板上led
led=Pin(2,Pin.OUT) #构建led对象，GPIO2,输出
while True:
    led.value(1)
    time.sleep_ms(500)
    led.value(0)
    time.sleep_ms(500)
