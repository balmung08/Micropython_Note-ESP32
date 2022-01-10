from machine import UART

uart=UART(2,115200) #设置串口号2和波特率

uart.write('Hello 01Studio!')#发送一条数据

while True:
    #判断有无收到信息
    if uart.any():
        text=uart.read(128) #接收128个字符
        print(text) #通过REPL打印串口3接收的数据
