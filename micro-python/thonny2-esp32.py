import socket
import network
import camera
import time
import os

# 连接wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('GloriStudioJD', 'qwer1234')
    
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

# 摄像头初始化
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)

# 其他设置：
camera.flip(1)  # 上翻下翻
camera.mirror(1)  # 左/右

# 设置分辨率为1080p
camera.framesize(camera.FRAME_FHD)

# 特效
camera.speffect(camera.EFFECT_NONE)

# 白平衡
# camera.whitebalance(camera.WB_HOME)

# 饱和
camera.saturation(0)

# 亮度
camera.brightness(0)

# 对比度
camera.contrast(0)

# 质量
camera.quality(10)

# socket UDP 的创建
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

# 文件保存相关
def save_image(image_data, filename):
    with open(filename, 'wb') as f:
        f.write(image_data)

def save_video(video_data, filename):
    with open(filename, 'wb') as f:
        f.write(video_data)

try:
    frame_count = 1
    video_buffer = b''
    start_time = time.time()
    
    while True:
        buf = camera.capture()  # 获取图像数据
        s.sendto(buf, ("192.168.68.175", 9090))  # 向服务器发送图像数据
        
        # 保存图像为JPEG文件
        image_filename = f"/sdcard/{frame_count:06d}.jpg"
        save_image(buf, image_filename)
        
        # 累积视频数据
        video_buffer += buf
        
        # 每分钟保存一次视频文件
        if time.time() - start_time >= 60:
            video_filename = f"/sdcard/{frame_count//6000:05d}.mp4"
            save_video(video_buffer, video_filename)
            video_buffer = b''
            start_time = time.time()
        
        frame_count += 1
        time.sleep(0.1)
except Exception as e:
    print(e)
finally:
    camera.deinit()
