import socket
import time

host = '192.168.88.15'
port = 5406

oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for _ in range(1, 101):
    for i in range(1, 11):
        message = "Packet " + str(format(i, '3d')) + " sended at t = " + str(format(time.time(), '.5f'))
        
        print(message)
        
        oSocket.sendto(message.encode('utf-8'), (host, port))
        
        time.sleep(0.1)

