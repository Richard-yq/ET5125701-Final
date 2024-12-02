import socket
import time
import threading
# 設定目標 IP 和 port  
host = '192.168.88.24'
port = 0

server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print('Receiver is ready')

recv_time = 0
counter = 1
def handle_client(client_socket):
    global recv_time, counter

    Rec_message, Rec_address = server.recv(65535)
    # message decode
    Rec_message = Rec_message.decode('utf-8')
    temp = Rec_message.split()

    # calulate the Pocket_duration
    trans_time_next = time.time()
    Pocket_duration = (trans_time_next - recv_time) * 1000 

    if recv_time == 0:
        Pocket_duration = 0

    print(str(format(counter, '3d')) + '=>' + Rec_message + ' |  Packet duration = ' + str(format(Pocket_duration, '1.5f')) + ' ms')

    client_socket.send(b"ACK!")

    print(client_socket.getpeername())
    client_socket.close()

    recv_time = trans_time_next
    counter += 1
    
while True:
    # 等待客戶端連線
    try:
        client, addr = server.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start() 

    except socket.timeout:
        print('Time out')
        break