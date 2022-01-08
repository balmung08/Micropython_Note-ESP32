from machine import I2C
from fpioa_manager import fm
import lcd, image
from Maix import GPIO
import touchscreen as ts

def draw():
    fm.register(16, fm.fpioa.GPIO1, force=True)
    btn_clear = GPIO(GPIO.GPIO1, GPIO.IN)
    i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
    ts.init(i2c)
    lcd.init(freq=15000000)
    lcd.clear()
    lcd.rotation(2)
    
    img = image.Image()
    status_last = ts.STATUS_IDLE
    x_last = 0
    y_last = 0
    x=100
    y=100
    draw = False
    
    while True:
        img.draw_rectangle(118, 0, 90, 10, fill = True)
        img.draw_string(120,0,"5-drawing board",color=(0,0,0))
        img.draw_string(0,0,"click here")
        img.draw_string(15,15,"clear")
        img.draw_rectangle(0, 0, 50, 30)
        (status,x,y) = ts.read()
        x=(320-x)
        y=(240-y)
        
        if draw:
            img.draw_line((x_last, y_last, x, y))
            
        x_last = x
        y_last = y
        
        if status_last!=status:
            if (status==ts.STATUS_PRESS or status == ts.STATUS_MOVE):
                draw = True
            else: 
                draw = False
            status_last = status
           
        lcd.display(img)
        if (x<50 and y<30):
            img.clear()
        
while(1):
    draw()
