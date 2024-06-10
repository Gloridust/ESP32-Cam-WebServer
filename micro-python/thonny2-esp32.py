import socket
import network
import camera
import time
import os
import sdcard
import machine

# 连接wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('GloriStudioJD', 'qwer1234')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

# 初始化SD卡
sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")
print("SD card initialized and mounted.")

# 摄像头初始化
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)

# 其他设置
camera.flip(1)
camera.mirror(1)
camera.framesize(camera.FRAME_FHD)  # 设置为1080p
camera.speffect(camera.EFFECT_NONE)
camera.saturation(0)
camera.brightness(0)
camera.contrast(0)
camera.quality(10)

# 初始化计时器和文件计数器
start_time = time.time()
file_count = 1
file_path = "/sd/"

try:
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # 每分钟保存一个新的视频文件
        if elapsed_time >= 60:
            file_count += 1
            start_time = current_time
        
        buf = camera.capture()  # 获取图像数据
        file_name = "{:05d}.jpg".format(file_count)
        with open(file_path + file_name, "wb") as f:
            f.write(buf)
        
        time.sleep(0.1)
except Exception as e:
    print("An error occurred:", e)
finally:
    camera.deinit()
    os.umount("/sd")
    print("Camera deinitialized and SD card unmounted.")
