import cv2
import imutils
import socket
import numpy as np
import time
import base64
import threading
import os
from socket import *
os.system("sudo pigpiod")
time.sleep(1)
import pigpio

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '192.168.1.2'  # socket.gethostbyname(host_name)
print(host_ip)
port = 50005
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)

vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
fps, st, frames_to_count, cnt = (0, 0, 30, 0)

address = ('192.168.1.200', 5000)  # Define who you are talking to (must match Arduino IP and port)
client_socket = socket(AF_INET, SOCK_DGRAM)  # Set up the socket
client_socket.settimeout(1)  # Only wait 1 second for a response
rec_data = ''
final = ''

ESC = 17
ESC1 = 18

Count_ESC = [ESC, ESC1]
pi = pigpio.pi()
pi.set_servo_pulsewidth(17, 1500)
pi.set_servo_pulsewidth(18, 1500)
time.sleep(2)


def data():
    while True:  # Main Loop
        data = "1"  # Set data to Blue Command
        client_socket.sendto(str.encode(data), address)  # Send command to Arduino
        try:
            rec_data, addr = client_socket.recvfrom(2048)  # Read response from Arduino
            rec_data = rec_data.decode("utf-8")
            final = rec_data.split(',')
            pi.set_servo_pulsewidth(17, final[1])
            pi.set_servo_pulsewidth(18, final[1])
            print(final[3])
            print(final[2])
        except:
            pass


# Position = threading.Thread(target=data)
data().start()

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from', client_addr)
    WIDTH = 400
    while vid.isOpened():
        _, frame = vid.read()
        frame = imutils.resize(frame, width=WIDTH)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        server_socket.sendto(message, client_addr)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1

    if key == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
