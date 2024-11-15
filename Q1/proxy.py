import socket
import random
import time

host = '192.168.88.250' # Client IP
proxy_ip = '192.168.88.15' # Proxy PI eth3
port = 5406 # Proxy port
target_prot = 5407 # Client port


count = 0
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_ip, port))

N_time = 100 # Maximum number of packets

while True:
    recv_data, client_addr = c.recvfrom(65535)
    message = recv_data.decode('UTF-8')

    temp = message.split()
    flag = int(temp[1]) # Sequence number

    c.sendto(recv_data, (host, target_prot))

