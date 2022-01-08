'''
实验名称：Table(表格)
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
###############      Table   ################
#############################################

if TOUCH_READY:

    # Create a normal cell style
    style_cell1 = lv.style_t()
    lv.style_copy(style_cell1, lv.style_plain)
    style_cell1.body.border.width = 1
    style_cell1.body.border.color = lv.color_make(0,0,0)

    # Crealte a header cell style
    style_cell2 = lv.style_t()
    lv.style_copy(style_cell2, lv.style_plain)
    style_cell2.body.border.width = 1
    style_cell2.body.border.color = lv.color_make(0,0,0)
    style_cell2.body.main_color = lv.color_make(0xC0, 0xC0, 0xC0)
    style_cell2.body.grad_color = lv.color_make(0xC0, 0xC0, 0xC0)

    table = lv.table(lv.scr_act())
    table.set_style(lv.table.STYLE.CELL1, style_cell1)
    table.set_style(lv.table.STYLE.CELL2, style_cell2)
    table.set_style(lv.table.STYLE.BG, lv.style_transp_tight)
    table.set_col_cnt(2)
    table.set_row_cnt(4)
    table.align(None, lv.ALIGN.CENTER, 0, 0)

    # Make the cells of the first row center aligned
    table.set_cell_align(0, 0, lv.label.ALIGN.CENTER)
    table.set_cell_align(0, 1, lv.label.ALIGN.CENTER)

    # Make the cells of the first row TYPE = 2 (use `style_cell2`)
    table.set_cell_type(0, 0, 2)
    table.set_cell_type(0, 1, 2)

    # Fill the first column
    table.set_cell_value(0, 0, "Name")
    table.set_cell_value(1, 0, "Apple")
    table.set_cell_value(2, 0, "Banana")
    table.set_cell_value(3, 0, "Citron")

    # Fill the second column
    table.set_cell_value(0, 1, "Price")
    table.set_cell_value(1, 1, "$7")
    table.set_cell_value(2, 1, "$4")
    table.set_cell_value(3, 1, "$6")
