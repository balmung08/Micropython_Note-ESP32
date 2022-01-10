import machine, sdcard, os
SD_CS = machine.Pin(5)
sd = sdcard.SDCard(machine.SPI(2,sck=Pin(18), mosi=Pin(23),miso=Pin(19)), SD_CS)
os.mount(sd, "/sd")   # 挂载SD卡到/sd目录下
dirs=os.listdir('/sd')
