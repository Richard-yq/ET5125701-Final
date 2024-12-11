import socket
import ssl
import time

# sender:24
# receiver:250
sender_host = '192.168.88.24'
sender_port = 5407

receiver_ip = '192.168.88.250'
receiver_port = 5500

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create an SSL context
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# wrap the socket with the SSL context
ssl_client = context.wrap_socket(client, server_hostname=receiver_ip)

# connect the client
ssl_client.connect((receiver_ip, receiver_port))
print("Connected to the receiver")

for _ in range(1, 2):
    for i in range(1, 1000001):
        message = f"Packet {i:6d}\n"
        
        # print(message)
        
        ssl_client.sendall(message.encode('utf-8'))
        
        # time.sleep(0.0005)

# time.sleep(2)
# receive data
response = ssl_client.recv(65335)

# print(response.decode())
ssl_client.close()