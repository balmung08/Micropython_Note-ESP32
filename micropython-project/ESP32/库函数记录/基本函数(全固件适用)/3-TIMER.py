from machine import Pin,Timer
import time
led=Pin(2,Pin.OUT)
Counter = 0
Fun_Num = 0

# 定义回调函数
def fun(tim):
    global Counter
    Counter = Counter + 1
    print(Counter)
    led.value(Counter%2)

#开启RTOS定时器，编号任选，不重复即可
tim = Timer(1)

# 周期单位ms，mode有Timer.ONE_SHOT 执行一次，Timer.PERIODIC 周期
tim.init(period=1000, mode=Timer.PERIODIC,callback=fun)

#定时器为独立函数，可与主函数同时执行
while True:
    print("doing")
    time.sleep(0.5)