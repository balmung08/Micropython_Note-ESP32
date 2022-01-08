from machine import Pin, I2C
from machine import Pin, SPI


# 在给定的引脚上创建SPI总线
# （极性）polarity是指 SCK 空闲时候的状态
# （相位）phase=0 表示SCK在第1个边沿开始取样，phase=1 表示在第2个边沿开始。
hspi = SPI(1, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
#hspi与vspi完全一样，是区分两个spi通道的叫法
vspi.init()              # 初始化spi
vspi.read(10)            # 在MISO引脚读取10字节数据
vspi.read(10, 0xff)      # 在MISO引脚读取10字节数据同时在MOSI输出0xff
buf = bytearray(50)     # 建立缓冲区
vspi.readinto(buf)       # 读取数据并存放在缓冲区 (这里读取50个字节)
vspi.readinto(buf, 0xff) # 读取数据并存放在缓冲区，同时在MOSI输出0xff
vspi.write(b'12345')     # 在MOSI引脚上写5字节数据
buf = bytearray(4)      # 建立缓冲区
vspi.write_readinto(b'1234', buf) # 在MOSI引脚上写数据并将MISO读取数据存放到缓冲区
vspi.write_readinto(buf, buf) # 在MOSI引脚上写缓冲区的数据并将MISO读取数据存放到缓冲区



# 构建一个I2C 总线 scl和sda可自设
i2c0 = I2C(0, scl=Pin(25), sda=Pin(26), freq=400000)
i2c1 = I2C(1, scl=Pin(18), sda=Pin(19), freq=400000)
print(i2c0.scan())              # 扫描从设备
'''
# 假设iic外设地址为0x3a
i2c.readfrom(0x3a, 4)   # 从地址为0x3a的从机设备读取4字节数据
buf = bytearray(10)     # 创建1个10字节缓冲区
i2c.writeto(0x3a, buf)  # 写入缓冲区数据到从机
i2c.writeto(0x3a, '12') # 向地址为0x3a的从机设备写入数据"12"
'''

