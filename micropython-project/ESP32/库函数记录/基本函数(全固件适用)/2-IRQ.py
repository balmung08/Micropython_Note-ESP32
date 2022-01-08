from machine import Pin
import time

# 测试时连接pin22与pin23

LED=Pin(2,Pin.OUT) #构建LED对象,开始熄灭
pin_interrupt=Pin(23,Pin.IN,Pin.PULL_UP) #构建外部中断触发引脚(使能上拉电阻)
pin_signal=Pin(22,Pin.OUT) #构建外部中断触发信号引脚
led_status=0

# 中断服务函数
def fun(pin_interrupt):
    print("irq triggered")

pin_interrupt.irq(fun,Pin.IRQ_FALLING) #定义中断，下降沿触发 (IRQ_RISING为上升沿）
# IRQ_LOW_LEVEL(低电平触发) IRQ_HIGH_LEVEL(高电平触发)


while True:
    # 改变led状态并输出
    if led_status == 0:
        led_status=1
    elif led_status == 1:
        led_status=0
    print("led:",led_status)
    LED.value(led_status)
    # 产生中断信号
    pin_signal(led_status)
    time.sleep(1)

