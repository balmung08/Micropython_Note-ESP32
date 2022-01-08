import _thread #导入线程模块
import time


i = 0
#线程函数
def func1():
    _thread.start_new_thread(func2,()) #开启线程2,参数必须是元组
    while True:
        print("main doing")
        time.sleep(0.5)
 
def func2():
    global i
    print("go")
    while True:
        print(i)
        i += 1
        time.sleep(0.5)
        if i==10:
            print("thread2 exit")
            _thread.exit()
            
           
#注意函数名和形参输入要拆开写
_thread.start_new_thread(func1,()) #开启线程1,参数必须是元组


    