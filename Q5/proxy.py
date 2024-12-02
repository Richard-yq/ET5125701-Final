import socket
import random
import time

host = '192.168.88.250' # Client IP
proxy_ip = '192.168.88.15' # Proxy PI eth3
port = 5406 # Proxy port
target_port = 5407 # Client port

count = 0
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind((proxy_ip, port))
c.listen(5)

N_time = 1000 # Maximum number of packets

while True:
    recv_data, client_addr = c.recv(65536)
    message = recv_data.decode('UTF-8')

    temp = message.split()
    flag = int(temp[1]) # Sequence number

    c.sendto(recv_data, (host, target_port))