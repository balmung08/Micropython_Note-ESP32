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


def ui_show_object(target,x,y,thres,text,fps,time_start):
    lcd.draw_string(0,0,"--status--",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(120,0,"1-number detection",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,20,"fps:"+fps,lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,40,"size:224*224",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,60,"target:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,80,target,lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,100,"position:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,120,"("+str(x)+","+str(y)+")",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,140,"model:yolov2",lcd.WHITE, lcd.BLACK)
    time_now = utime.mktime(utime.localtime())-time_start
    lcd.draw_string(0,160,"time:"+str(time_now)+"s",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,180,"TH:"+str(thres),lcd.WHITE, lcd.BLACK)  
    lcd.draw_string(0,200,"label:"+str(text),lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,215,"------------",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,225,"by:balmung",lcd.WHITE, lcd.BLACK)


def object_detection_main(anchors, labels = None):
    thres=0.7
    text="/"
    x=0
    y=0
    target="number"
    lcd.init(freq=15000000)
    sensor.reset()                      
    sensor.set_pixformat(sensor.RGB565) 
    sensor.set_framesize(sensor.QVGA)   
    sensor.set_windowing((224,224))
    sensor.set_hmirror(False)
    sensor.set_vflip(False)
    sensor.run(1)
    lcd.rotation(2)
    time_start = utime.mktime(utime.localtime())
    clock = time.clock()                # Create a clock object to track the FPS
    img = image.Image("startup.jpg")
    lcd.display(img)
    task = kpu.load("/sd/number.kmodel")
    kpu.init_yolo2(task, thres, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
    lcd.clear()
    try:
        while 1:
            clock.tick() 
            img = sensor.snapshot()
            img.draw_rectangle(0, 0, 224, 224, color = (255, 255, 255), thickness = 2, fill = False)
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            fps=str(int(clock.fps()))
            if objects:
                for obj in objects:
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 0, 0))
                    text=labels[obj.classid()]
                    x=obj.x()
                    y=obj.y()                   
            else:
                text="/"
                x=0
                y=0         
            img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
            lcd.fill_rectangle(0, 120, 70, 12, lcd.WHITE)
            lcd.display(img,roi=(0,0,224,224),oft=(96, 16))
            ui_show_object(target,x,y,thres,text,fps,time_start)
            if KEY.value()==0:
                return 0
    except Exception as e:
        raise e
    finally:
        kpu.deinit(task)
       

def object_detection():
    labels = ['1', '2', '3', '4', '5', '6', '7', '8']
    anchors = [1.40625, 1.8125000000000002, 5.09375, 5.28125, 3.46875, 3.8124999999999996, 2.0, 2.3125, 2.71875, 2.90625]
    object_detection_main(anchors = anchors, labels=labels)


if __name__ == "__main__":
    try:
        while(1): 
                object_detection()

    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
