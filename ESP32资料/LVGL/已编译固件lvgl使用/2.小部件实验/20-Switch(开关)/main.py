'''
实验名称：Switch(开关)
版本：v1.0
日期：2020.7
作者：01Studio【www.01Studio.org】
'''

import lvgl as lv
import ujson

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

#############################################
###############      Switch   ###############
#############################################
def event_handler(obj, event):
    if event == lv.EVENT.VALUE_CHANGED:
        print("State: %s" % ("On" if obj.get_state() else "Off"))

if TOUCH_READY:

    # Create styles for the switch
    bg_style = lv.style_t()
    indic_style = lv.style_t()
    knob_on_style = lv.style_t()
    knob_off_style = lv.style_t()

    lv.style_copy(bg_style, lv.style_pretty)
    bg_style.body.radius = 800
    bg_style.body.padding.top = 6
    bg_style.body.padding.bottom = 6

    lv.style_copy(indic_style, lv.style_pretty_color)
    indic_style.body.radius = 800
    indic_style.body.main_color = lv.color_hex(0x9fc8ef)
    indic_style.body.grad_color = lv.color_hex(0x9fc8ef)
    indic_style.body.padding.left = 0
    indic_style.body.padding.right = 0
    indic_style.body.padding.top = 0
    indic_style.body.padding.bottom = 0

    lv.style_copy(knob_off_style, lv.style_pretty)
    knob_off_style.body.radius = 800
    knob_off_style.body.shadow.width = 4
    knob_off_style.body.shadow.type = lv.SHADOW.BOTTOM

    lv.style_copy(knob_on_style, lv.style_pretty_color)
    knob_on_style.body.radius = 800
    knob_on_style.body.shadow.width = 4
    knob_on_style.body.shadow.type = lv.SHADOW.BOTTOM

    # Create a switch and apply the styles
    sw1 = lv.sw(lv.scr_act())
    sw1.set_style(lv.sw.STYLE.BG, bg_style)
    sw1.set_style(lv.sw.STYLE.INDIC, indic_style)
    sw1.set_style(lv.sw.STYLE.KNOB_ON, knob_on_style)
    sw1.set_style(lv.sw.STYLE.KNOB_OFF, knob_off_style)
    sw1.align(None, lv.ALIGN.CENTER, 0, -50)
    sw1.set_event_cb(event_handler)

    # Copy the first switch and turn it ON
    sw2 = lv.sw(lv.scr_act(), sw1)
    sw2.on(lv.ANIM.ON)
    sw2.align(None, lv.ALIGN.CENTER, 0, 50)
    sw2.set_event_cb(lambda o,e: None)
