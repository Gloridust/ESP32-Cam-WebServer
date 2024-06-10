import socket
import network
import camera
import time


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
# 上翻下翻
camera.flip(1)
#左/右
camera.mirror(1)

# 分辨率
camera.framesize(camera.FRAME_HVGA)
# 选项如下：
# FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
# FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
# FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
# FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
# FRAME_P_FHD FRAME_QSXGA

# 特效
camera.speffect(camera.EFFECT_NONE)
#选项如下：
# 效果\无（默认）效果\负效果\ BW效果\红色效果\绿色效果\蓝色效果\复古效果
# EFFECT_NONE (default) EFFECT_NEG \EFFECT_BW\ EFFECT_RED\ EFFECT_GREEN\ EFFECT_BLUE\ EFFECT_RETRO

# 白平衡
# camera.whitebalance(camera.WB_HOME)
#选项如下：
# WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

# 饱和
camera.saturation(0)
#-2,2（默认为0）. -2灰度
# -2,2 (default 0). -2 grayscale 

# 亮度
camera.brightness(0)
#-2,2（默认为0）. 2亮度
# -2,2 (default 0). 2 brightness

# 对比度
camera.contrast(0)
#-2,2（默认为0）.2高对比度
#-2,2 (default 0). 2 highcontrast

# 质量
camera.quality(10)
#10-63数字越小质量越高

# socket UDP 的创建
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)

try:
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # 每分钟保存一个新的视频文件
        if elapsed_time >= 60:
            file_count += 1
            start_time = current_time
        
        buf = camera.capture()  # 获取图像数据
        s.sendto(buf, ("192.168.68.175", 9090))  # 向服务器发送图像数据
        time.sleep(0.1)
except:
    pass
finally:
    camera.deinit()

