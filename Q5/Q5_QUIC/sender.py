import socket
import time

# sender:24
# receiver:250
sender_host = '192.168.88.24'
sender_port = 5407

receiver_ip = '192.168.88.250'
receiver_port = 5500
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((receiver_ip, receiver_port))

for _ in range(1, 11):
    for i in range(1, 11):
        message = "Packet " + str(format(i, '3d')) + " sended at t = " + str(format(time.time(), '.5f'))
        
        print(message)
        
        client.sendto(message.encode('utf-8'), (receiver_ip, receiver_port))
        
        time.sleep(0.1)
# receive data
response = client.recv(65335)

print(response.decode())
client.close()