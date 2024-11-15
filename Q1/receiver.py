import socket
import time

# 設定目標 IP 和 port  
host = '192.168.88.250'
port = 5407

oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
oSocket.bind((host, port))

# time_out_time = 10
# oSocket.settimeout(time_out_time)

print('Receiver is ready')

recv_time = 0
counter = 1
while True:
    try:
        Rec_message, Rec_address = oSocket.recvfrom(65535)
        

        Rec_message = Rec_message.decode('utf-8')
        temp = Rec_message.split()

        trans_time_next = time.time()
        Pocket_duration = (trans_time_next - recv_time) * 1000 

        if recv_time == 0:
            Pocket_duration = 0

        print(str(format(counter, '3d')) + '=>' + Rec_message + ' |  Packet duration = ' + str(format(Pocket_duration, '1.5f')) + ' ms')
        recv_time = trans_time_next
        counter += 1
    except socket.timeout:
        print('Time out')
        break