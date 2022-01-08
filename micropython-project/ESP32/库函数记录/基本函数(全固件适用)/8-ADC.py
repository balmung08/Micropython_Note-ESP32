#导入相关模块
from machine import Pin,I2C,ADC,Timer,DAC
import utime, math,time

#初始化ADC
adc = ADC(Pin(33),bits=12)
adc.atten(ADC.ATTN_11DB)#配置衰减器。配置衰减器能增加电压测量范围，但是以精度为代价的。
'''
ADC.ATTN_0DB： 0dB 衰减, 最大输入电压为 1.00v 默认配置；
ADC.ATTN_2_5DB： 2.5dB 衰减, 最大输入电压约为 1.34v；
ADC.ATTN_6DB：6dB 衰减, 最大输入电压约为 2.00v；
ADC.ATTN_11DB：11dB 衰减, 最大输入电压约为 3.3v。
'''

#初始化DAC
dac = DAC(Pin(25,Pin.OUT), bits=8) # bit 为分辨率位数

i=0
while True:
    dac_value = abs(255 * math.sin(i))
    dac.write(int(dac_value))#dac输出幅值（有零阶保持器）
    print("adc-v:",adc.read()/4095*3.3,)#获取 ADC 值。测量精度是 12 位，返回 0-4095（表示 0-3.3V）
    print("dac-v:",int(dac_value)/255*3.3)
    print("-"*20)
    i += 0.2
    time.sleep(0.3)

# 可见dac和adc之间有一定误差