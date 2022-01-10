from machine import Pin, I2C, RTC,Timer

# 定义星期和时间（时分秒）显示字符列表
week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
time_list = ['', '', '']

# 初始化rtc
rtc = RTC()
#rtc.init((2014, 5, 1, 4, 13, 0, 0, 0))
#初始化rtc时间 (年月日/星期/时分秒/时区对象)
def RTC_Run(tim):
    datetime = rtc.datetime()  # 获取当前时间
    print(datetime)
    
#开启RTOS定时器
tim = Timer(1)
tim.init(period=500, mode=Timer.PERIODIC, callback=RTC_Run) #周期500ms
