from machine import Pin, PWM
import time

#PWM 可以通过 ESP32 所有 GPIO 引脚输出. 所有通道都有 1 个特定的频率，从 1 到 40M 之间（单位是 Hz）

# 构建 PWM 对象。id:引脚编号；freq:频率值；duty:占空比；配置完后 PWM 自动生效。
Beep = PWM(Pin(13), freq=1000, duty=1000) # 在同一语句下创建和配置PWM并直接开始发出波形
time.sleep_ms(1000)

Beep.duty(500) # 设置占空比。duty:占空比在 0-1023 之间，duty 为空时表示获取当前占空比值。
time.sleep_ms(1000)

Beep.freq(500) # freq:频率值在 1-1000 之间
time.sleep_ms(1000)

Beep.deinit() # 停止