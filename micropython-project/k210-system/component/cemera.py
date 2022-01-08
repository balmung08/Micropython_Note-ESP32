import sensor, image, time, lcd
import utime
import KPU as kpu
import gc, sys
from Maix import GPIO
from fpioa_manager import fm
from machine import I2C
import touchscreen as ts

def take_photos():
    img = image.Image("startup.jpg")
    lcd.display(img)
    sensor.reset()                      
    sensor.set_pixformat(sensor.RGB565) 
    sensor.set_framesize(sensor.QVGA)   
    sensor.set_windowing((224,224))
    sensor.set_hmirror(False)
    sensor.set_vflip(False)
    sensor.run(1)
    lcd.rotation(2)
    i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
    ts.init(i2c)
    time_start = utime.mktime(utime.localtime())
    clock = time.clock()             
    x=320
    y=240
    x_last = 0
    y_last = 0
    i=0
    status_last = ts.STATUS_IDLE
    lcd.clear()
    while(True):
        clock.tick() 
        img = sensor.snapshot()
        (status,x,y) = ts.read()
        x=(320-x)
        y=(240-y)
        if (0<x<90 and 180<y<226 and status==ts.STATUS_PRESS):
            sensor.snapshot().save("/sd/"+str(i)+".jpg")
            i += 1
        img.draw_rectangle(0, 0, 224, 224, color = (255, 255, 255), thickness = 2, fill = False)
        lcd.fill_rectangle(0, 60, 70, 12, lcd.WHITE)
        ui_show_photos(i)
        lcd.display(img,roi=(0,0,224,224),oft=(96, 16))
        if KEY.value()==0:
            return 0
        print(x,y,i)

def ui_show_photos(note):
    lcd.draw_string(0,0,"--status--",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(120,0,"6-cemera",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,20,"size:224*224",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,40,"pic_number:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,60,str(note),lcd.BLACK, lcd.WHITE)
    get = image.Image("cemera.jpg")
    lcd.display(get,oft=(0, 180))
    lcd.draw_string(0,140,"------------",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,160,"by:balmung",lcd.WHITE, lcd.BLACK)

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

if __name__ == "__main__":
    try:
        while(1):
            take_photos(）           
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
