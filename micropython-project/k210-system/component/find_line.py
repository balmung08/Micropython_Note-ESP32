import sensor, image, time, lcd
import utime
import KPU as kpu
import gc, sys
from Maix import GPIO
from fpioa_manager import fm


def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

    
def find_line():
    target="line"
    side=0
    grey_threshold   = (0, 70)
    lcd.init(freq=15000000)
    sensor.reset()                      
    sensor.set_pixformat(sensor.GRAYSCALE) 
    sensor.set_framesize(sensor.QVGA)   
    sensor.set_hmirror(False)
    sensor.set_vflip(False)
    sensor.run(1)
    sensor.set_windowing((224,224))
    lcd.rotation(2)
    sensor.set_auto_gain(False)
    sensor.set_auto_whitebal(False) # turn this off.
    time_start = utime.mktime(utime.localtime())
    clock = time.clock()                # Create a clock object to track the FPS
    img = image.Image("startup.jpg")
    lcd.display(img)
    time.sleep_ms(500)
    lcd.clear()
    while(1):
        clock.tick()
        img = sensor.snapshot()
        img.draw_rectangle(0, 0, 224, 224, color = (255, 255, 255), thickness = 2, fill = False)
        fps=str(int(clock.fps()))
        line = img.get_regression([grey_threshold],robust = False)
        if (line):
            img.draw_line(line.line(), color = 127)
            th = line.theta()
            if th > 90:
                th = 180 - th
                side="L"
            else:   
                side="R"
            distance = abs(line.rho())-img.width()/2
        lcd.fill_rectangle(0, 200, 70, 12, lcd.WHITE)
        ui_show_line(target,th,fps,time_start,side,distance)    
        lcd.display(img,roi=(0,0,224,224),oft=(96, 16))
        if KEY.value()==0:
            return 0


def ui_show_line(target,theta,fps,time_start,side,distance):
    lcd.draw_string(0,0,"--status--",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(120,0,"3-findline",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,20,"fps:"+fps,lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,40,"size:224*224",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,60,"target:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,80,target,lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,100,"theta:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,120,str(theta),lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,140,"regression",lcd.WHITE, lcd.BLACK)
    time_now = utime.mktime(utime.localtime())-time_start
    lcd.draw_string(0,160,"time:"+str(time_now)+"s",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,180,"side:"+str(side),lcd.WHITE, lcd.BLACK)  
    lcd.draw_string(0,200,"dist:"+str(int(distance)),lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,215,"------------",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,225,"by:balmung",lcd.WHITE, lcd.BLACK)


if __name__ == "__main__":
    try:
        while(1):
            find_line()
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
