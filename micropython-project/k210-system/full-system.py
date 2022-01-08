import sensor, image, time, lcd
import utime
import KPU as kpu
import gc, sys
from Maix import GPIO
from fpioa_manager import fm
from machine import I2C
import touchscreen as ts

fm.register(16, fm.fpioa.GPIO1)
KEY = GPIO(GPIO.GPIO1, GPIO.IN)

def show_init():
    lcd.draw_string(0,0,"--list--",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,20,"mode1:number detection",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,40,"mode2:human detection",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,60,"mode3:find line",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,80,"mode4:canny edge exteaction",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,100,"mode5:drawing board",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,120,"mode6:cemera",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,140,"press button to change mode",lcd.WHITE, lcd.BLACK)
    

def start_menu():
    lcd.init(freq=15000000)
    lcd.clear()
    lcd.rotation(2)
    img = image.Image("startup.jpg")
    lcd.display(img)
    time.sleep_ms(500)
    lcd.clear()
    while(1):
        show_init()
        if KEY.value()==0:
            return 0
            

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
    img = image.Image("startup.jpg")
    lcd.display(img)
    thres=0.7
    text="/"
    x=0
    y=0
    target="number"
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
    

def human_detection_main(anchors):
    img = image.Image("startup.jpg")
    lcd.display(img)
    thres=0.5
    text="/"
    x=0
    y=0
    target="human"
    sensor.reset()                      
    sensor.set_pixformat(sensor.RGB565) 
    sensor.set_framesize(sensor.QVGA)   
    sensor.set_hmirror(False)
    sensor.set_vflip(False)
    sensor.run(1)
    lcd.rotation(2)
    time_start = utime.mktime(utime.localtime())
    clock = time.clock()                # Create a clock object to track the FPS

    task = kpu.load("/sd/facedetect.kmodel") 
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchors)
    lcd.clear()
    try:
        while(1):
            clock.tick()
            img = sensor.snapshot()
            img.draw_rectangle(0, 0, 224, 224, color = (255, 255, 255), thickness = 2, fill = False)
            human = kpu.run_yolo2(task, img) 
            fps=str(int(clock.fps()))
            if human:
                for i in human:
                    b = img.draw_rectangle(i.rect())
                    x=i.x()
                    y=i.y()
                    text=1
            else:
                x=0
                y=0
                text="/"
            #img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
            lcd.fill_rectangle(0, 120, 70, 12, lcd.WHITE)
            lcd.display(img,roi=(0,0,224,224),oft=(96, 16))
            ui_show_human(target,x,y,thres,text,fps,time_start)
            if KEY.value()==0:
                return 0
    except Exception as e:
        raise e
    finally:
        kpu.deinit(task)


def human_detection():
    anchors = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    human_detection_main(anchors = anchors)


def ui_show_human(target,x,y,thres,text,fps,time_start):
    lcd.draw_string(0,0,"--status--",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(120,0,"2-human detection",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,20,"fps:"+fps,lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,40,"size:320*240",lcd.WHITE, lcd.BLACK)
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


def find_line():
    img = image.Image("startup.jpg")
    lcd.display(img)
    target="line"
    side=0
    grey_threshold   = (0, 70)
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
   

def edge_detection():
    img = image.Image("startup.jpg")
    lcd.display(img)
    thresholds = [(100, 255)]
    kernel_size = 1 # kernel width = (size*2)+1, kernel height = (size*2)+1
    kernel = [-1, -1, -1,\
              -1, +8, -1,\
              -1, -1, -1]
    target="edge"
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
    lcd.clear()
    while(True):
        clock.tick() 
        img = sensor.snapshot()   
        img.draw_rectangle(0, 0, 224, 224, color = (255, 255, 255), thickness = 2, fill = False)
        fps=str(int(clock.fps()))
        img.morph(kernel_size, kernel)
        img.binary(thresholds)
        img.erode(1, threshold = 2)
        lcd.display(img,roi=(0,0,224,224),oft=(96, 16))
        ui_show_edge(target,fps,time_start)
        if KEY.value()==0:
            return 0


def ui_show_edge(target,fps,time_start):
    lcd.draw_string(0,0,"--status--",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(120,0,"4-edge detection",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,20,"fps:"+fps,lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,40,"size:224*224",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,60,"target:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,80,target,lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,100,"thresholds:",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,120,"[100, 255]",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(0,140,"model:canny",lcd.WHITE, lcd.BLACK)
    time_now = utime.mktime(utime.localtime())-time_start
    lcd.draw_string(0,160,"time:"+str(time_now)+"s",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,180,"kernelsize:1",lcd.WHITE, lcd.BLACK) 
    lcd.draw_string(0,200,"erode-TH:2",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,215,"------------",lcd.WHITE, lcd.BLACK)
    lcd.draw_string(0,225,"by:balmung",lcd.WHITE, lcd.BLACK)
    

def draw():
    img = image.Image("startup.jpg")
    lcd.display(img)
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
    img.clear()
    lcd.clear()
    while True:
        img.draw_rectangle(118, 0, 90, 10, fill = True)
        img.draw_string(120,0,"5-drawing board",color=(0,0,0))
        img.draw_string(0,0,"click here")
        img.draw_string(15,15,"clear")
        img.draw_rectangle(0, 0, 50, 30)
        (status,x,y) = ts.read()
        x=(320-x)
        y=(240-y)
        if KEY.value()==0:
            return 0
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


if __name__ == "__main__":
    try:
        mode=0
        while(1):
            if mode == 0:
                start_menu()
                mode += 1
            if mode == 1:      
                object_detection()
                mode += 1
            if mode == 2:
                human_detection()
                mode += 1
            if mode == 3:
                find_line()
                mode += 1
            if mode == 4:
                edge_detection()
                mode += 1
            if mode == 5:
                draw()
                mode += 1
            if mode == 6:
                take_photos()
                mode += 1
            if mode == 7:
                mode = 0
                
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
