import network
import socket
import camera
import uos
from machine import SDCard
import time
import gc

# 设置 AP 模式
ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.active(True)
ap.config(essid='esp32', authmode=network.AUTH_WPA_WPA2_PSK, password='qwer1234')

print('AP 模式已启动')
print('网络配置:', ap.ifconfig())

# 初始化摄像头
camera.init(0, format=camera.JPEG)
camera.framesize(camera.FRAME_VGA)

# 尝试挂载 SD 卡
sd_available = False
try:
    uos.mount(SDCard(), "/sd")
    sd_available = True
    print("SD 卡挂载成功")
except Exception as e:
    print("SD 卡挂载失败:", e)

frame_count = 0

def web_page():
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>ESP32-CAM Stream</title>
        <style>
            img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>ESP32-CAM Stream</h1>
        <img src="/stream" id="stream">
        <script>
            var img = document.getElementById("stream");
            function updateImage() {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', "/stream", true);
                xhr.responseType = 'blob';
                xhr.onload = function(e) {
                    if (this.status == 200) {
                        var blob = this.response;
                        img.src = URL.createObjectURL(blob);
                    }
                };
                xhr.send();
            }
            setInterval(updateImage, 100);
        </script>
    </body>
    </html>
    """
    return html

def send_frame(conn):
    frame = camera.capture()
    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-Type: image/jpeg\r\n')
    conn.send(f'Content-Length: {len(frame)}\r\n'.encode())
    conn.send(b'\r\n')
    conn.sendall(frame)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Web 服务器已启动')

    global frame_count

    while True:
        conn, addr = s.accept()
        print('客户端连接:', addr)
        try:
            request = conn.recv(1024).decode()
            
            if 'GET /stream' in request:
                send_frame(conn)
                
                # 如果 SD 卡可用，保存图像
                if sd_available:
                    with open(f'/sd/frame_{frame_count}.jpg', 'wb') as f:
                        f.write(camera.capture())
                    frame_count += 1
            
            elif 'GET /' in request:
                conn.send('HTTP/1.1 200 OK\r\n')
                conn.send('Content-Type: text/html\r\n')
                conn.send('\r\n')
                conn.sendall(web_page())
            
        except Exception as e:
            print("Error handling request:", e)
        finally:
            conn.close()
        
        gc.collect()  # 进行垃圾回收

if __name__ == '__main__':
    main()