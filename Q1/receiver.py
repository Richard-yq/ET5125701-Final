import socket
import time

# 設定目標 IP 和 port  
host = '192.168.88.250'
port = 5407

oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
oSocket.bind((host, port))

time_out_time = 10
oSocket.settimeout(time_out_time)

while True:
    try:
        Rec_message, Rec_address = oSocket.recvfrom(65535)
        recv_time = time.time()

        Rec_message = Rec_message.decode('utf-8')
        temp = Rec_message.split()

        trans_time = float(temp[6])
        Pocket_delay = (recv_time - trans_time) * 1000 

        print(Rec_message + ' | pocket delay = ' + str(format(Pocket_delay, '1.5f')) + ' ms')

    except socket.timeout:
        print('Time out')
        break