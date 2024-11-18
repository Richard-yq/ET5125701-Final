import socket
import random
import time
import threading

host = '192.168.88.250' # Client IP
proxy_ip = '192.168.88.15' # Proxy PI eth3
port1 = 5406 # Proxy port
port2 = 5408
path1_client_port = 5405 # path1 Client port
path2_client_port = 5407 # path2 Client port


count = 0

N_time = 1000 # Maximum number of packets

def proxy(target_port, port):
    print("123")
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.bind((proxy_ip, port)) # c1 start
    while True:
        recv_data, client_addr = c.recvfrom(65535) # 65535: data lens (2^16)

        c.sendto(recv_data, (host, target_port)) 

path1 = threading.Thread(target=proxy, args=(path1_client_port,port1, ))
path2 = threading.Thread(target=proxy, args=(path2_client_port,port2, ))

path1.start()
path2.start()
