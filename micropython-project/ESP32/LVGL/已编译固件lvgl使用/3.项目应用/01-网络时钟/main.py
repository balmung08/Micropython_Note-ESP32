'''
实验名称：NTP(网络时钟)
版本：v1.0
日期：2020.7
作者：01Studio 【www.01Studio.org】
'''
import ntptime,network,dht
from machine import RTC,Pin

import lvgl as lv
import time,ujson

from ili9341 import ili9341
from xpt2046 import xpt2046

TFT_IS_PORTRAIT =1 #竖屏：1 ，横屏：0 ；
TOUCH_READY = 0 #用于检测触摸屏是否已经校准过；

#LCD ili9341初始化
disp = ili9341(
    miso=12,
    mosi=13,
    clk=14,
    cs=15,
    dc=21,
    rst=33,
    power=50,  #硬件不支持，随便配一个参数
    backlight=51, #硬件不支持，随便配一个参数
    backlight_on= 1,
    power_on= 1,
    width=240 if TFT_IS_PORTRAIT else 320,
    height=320 if TFT_IS_PORTRAIT else 240,
    rot=ili9341.PORTRAIT if TFT_IS_PORTRAIT else ili9341.LANDSCAPE #垂直方向PORTRAIT ；水平方向：LANDSCAPE
)

#触摸屏设置校准
TOUCH_CS = 2  #触摸屏CS片选引脚
TOUCH_INTERRUPT=0 #横屏

if TFT_IS_PORTRAIT:
    TOUCH_CALI_FILE = "touch_cali_PORTRAIT.json" #保存为竖屏触摸参数
else:
    TOUCH_CALI_FILE = "touch_cali_LANDSCAPE.json" #保存为横屏触摸参数

#从没做过触摸校准
if TOUCH_CALI_FILE not in uos.listdir():
    touch = xpt2046(
        cs=TOUCH_CS,
        transpose=TFT_IS_PORTRAIT,
    )

    from touch_cali import TouchCali

    touch_cali = TouchCali(touch, TOUCH_CALI_FILE)
    touch_cali.start()

#已经做过触摸校准，直接调用触摸参数文件
else:
    with open(TOUCH_CALI_FILE, 'r') as f:
        param = ujson.load(f)
        touch_x0 = param['cal_x0']
        touch_x1 = param['cal_x1']
        touch_y0 = param['cal_y0']
        touch_y1 = param['cal_y1']

    touch = xpt2046(
        cs=TOUCH_CS,
        transpose=TFT_IS_PORTRAIT,
        cal_x0=touch_x0,
        cal_x1=touch_x1,
        cal_y0=touch_y0,
        cal_y1=touch_y1,
    )

    TOUCH_READY = 1 #表示已经配置好触摸参数

d = dht.DHT11(Pin(27)) #传感器连接到引脚27

#RTC初始化
# 定义星期和时间（时分秒）显示字符列表
week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
time_list = ['', '', '']
rtc = RTC()

#WIFI连接函数,连接成功后更新时间
def WIFI_Connect():

    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('01Studio', '88888888') #输入WIFI账号密码

        while not wlan.isconnected():

            #超时判断,15秒没连接成功判定为超时
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():

        #串口打印信息
        print('network information:', wlan.ifconfig())

        for i in range(5): #最多尝试获取5次时间
            try:
                ntptime.settime()
                print(rtc.datetime())
                time.sleep_ms(500)
                return None

            except:
                print("Can not get time!")

#############################################
################Basic Object#################
#############################################
if TOUCH_READY:

    WIFI_Connect() #连接WiFi

    #Create a style based on style_plain
    mystyle = lv.style_t(lv.style_plain)
    #mystyle.text.font = roboto_80 # font roboto 80 pixel
    mystyle.text.font = lv.font_roboto_28
    mystyle.body.main_color = lv.color_hex(0x000000) # background top color (main), 0xRRGGBB
    mystyle.body.grad_color = lv.color_hex(0x000000) # background bottom color (gradient), 0xRRGGBB
    mystyle.text.color = lv.color_hex(0xffffff) # text-colour, 0xRRGGBB


    #Create screen and labels
    scr = lv.obj()
    scr.set_style(mystyle)

    LOGO = lv.label(scr)
    LOGO.set_pos(0,0)
    LOGO.set_drag(True)
    LOGO.set_text("01Studio")

    WIFI_ICON = lv.label(scr)
    WIFI_ICON.set_pos(200,0)
    WIFI_ICON.set_drag(True)
    WIFI_ICON.set_text(lv.SYMBOL.WIFI)

    DATE = lv.label(scr)
    DATE.set_pos(0,64)
    DATE.set_drag(True)

    TIME = lv.label(scr)
    TIME.set_pos(0,128)
    TIME.set_drag(True)

    TEMP = lv.label(scr)
    TEMP.set_pos(0,192)
    TEMP.set_drag(True)

    HUMI = lv.label(scr)
    HUMI.set_pos(0,256)
    HUMI.set_drag(True)

    a=0

#Create content
    while(1):

        datetime = list(rtc.datetime())  # 获取当前时间

        #北京时间，月、日、星期需要适当调整
        datetime[4]=datetime[4]+8 #北京时间，东八区
        if datetime[4] >= 24:
            datetime[4]=datetime[4]%24
            if datetime[1] in [1,3,5,7,8,10,12]: #大月
                datetime[2] = (datetime[2]+1)%32
            else: datetime[2] = (datetime[2]+1)%31
            datetime[3] = (datetime[3]+1)%8

        #显示日期
        DATE.set_text(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + week[datetime[3]])

        # 显示时间需要判断时、分、秒的值否小于10，如果小于10，则在显示前面补“0”以达
        # 到较佳的显示效果
        for i in range(4, 7):
            if datetime[i] < 10:
                time_list[i - 4] = "0"
            else:
                time_list[i - 4] = ""
        TIME.set_text(time_list[0] + str(datetime[4]) + ':' + time_list[1] + str(datetime[5]) + ':' + time_list[2] + str(datetime[6]))

        a=a+1 #控制DHT11采集时间，大于2秒间隔
        if a ==7:
            d.measure()         #温湿度采集
            a=0
            TEMP.set_text(str(d.temperature() )+' C')
            HUMI.set_text(str(d.humidity())+' %')

        # 300ms刷屏一次
        lv.scr_load(scr)
        time.sleep_ms(300)
