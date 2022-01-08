from machine import Pin,I2C,Timer
import onewire,ds18x20


#初始化DS18B20
ow= onewire.OneWire(Pin(4)) #使能单总线
ds = ds18x20.DS18X20(ow)        #传感器是DS18B20
rom = ds.scan()         #扫描单总线上的传感器地址，支持多个传感器同时连接
print(rom)
def temp_get(tim):
    ds.convert_temp()
    temp = ds.read_temp(rom[0]) #温度显示,rom[0]为第1个DS18B20
    print(temp)

#开启RTOS定时器，编号为-1
tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC,callback=temp_get) #周期为1000ms
