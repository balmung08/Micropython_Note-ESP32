from machine import DAC
from machine import Pin
import utime, math

# DAC在专用引脚上可用，可用的DAC引脚只有两个。 可用引脚有：GPIO25, GPIO26，输出的电压模拟值范围为0~3.3V

# 创建一个DAC的管脚Pin对象（声明为输出），然后传入到DAC的构造器里面
dac = DAC(Pin(26,Pin.OUT), bits=8) # bit 为分辨率位数
#ESP32的DAC分辨率只有8位，在MicroPython固件中12位的精度还未实现

i=0
while True:
    dac_value = abs(int(255 * math.sin(i)))
    dac.write(dac_value)#dac输出幅值（有零阶保持器）
    print(dac_value/255)
    i += 0.15

