import socket
import random
import time
import threading
import queue

host = '192.168.88.250' # Client IP
proxy_ip = '192.168.88.15' # Proxy PI eth3
port1 = 5406 # Proxy port
port2 = 5408
path1_client_port = 5405 # path1 Client port
path2_client_port = 5407 # path2 Client port

# Message queue for delayed packets
delay_queue = queue.Queue()
count = 0

N_time = 1000 # Maximum number of packets

def proxy_first(target_port, port): #  drops each received packet with 10% probability before forwarding to UDP Client.
    print("Open proxy_port: ", port)
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.bind((proxy_ip, port)) # c1 start
    count = 0  # Initialize the variable
    while True:
        recv_data, client_addr = c.recvfrom(65535) # 65535: data lens (2^16)
        message = recv_data.decode('UTF-8')

        temp = message.split()
        flag = int(temp[1]) # Sequence number

        # 0,0 <= pick <= 1,0
        pick = random.uniform(0,1)
        if pick <= 0.1: # 10% loss
            print("Packet loss, sequence number = ", flag)
            # Record the loss
            count += 1
        else:
            c.sendto(recv_data, (host, target_port))
        
        if flag == N_time:
            print("Total packets lost: ", count/N_time)
            break
        else:
            continue

def proxy_second(target_port, port): # delays 500 ms the received packet with 5% probability before forwarding to UDP Client.
    print("Open proxy_port: ", port)
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.bind((proxy_ip, port)) # c1 start
    while True:
        recv_data, client_addr = c.recvfrom(65535) # 65535: data lens (2^16)
        message = recv_data.decode('UTF-8')

        temp = message.split()
        flag = int(temp[1]) # Sequence number

        # 0,0 <= pick <= 1,0
        pick = random.uniform(0,1)
        if pick <= 0.05:  # 5% delay
            print("Packet queued for delay, sequence number = ", flag)
            delay_queue.put((recv_data, target_port))  # Add to queue
        else:
            c.sendto(recv_data, (host, target_port))
        
        if flag == N_time:
            break
        else:
            continue

def delay_handler():  # Handles delayed packets without blocking
    while True:
        recv_data, target_port = delay_queue.get()  # Fetch a delayed packet
        time.sleep(0.5)  # Simulate delay
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(recv_data, (host, target_port))
        print("Packet sent after delay")
        delay_queue.task_done()

path1 = threading.Thread(target=proxy_first, args=(path1_client_port,port1, ))
path2 = threading.Thread(target=proxy_second, args=(path2_client_port,port2, ))
delay_thread = threading.Thread(target=delay_handler, daemon=True)  # Run delay handler in the background


path1.start()
path2.start()
delay_thread.start()

