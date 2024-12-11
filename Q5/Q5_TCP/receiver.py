import socket
import time
import ssl
# 設定目標 IP 和 port  
host = '192.168.88.24'
port = 5500

server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print('Receiver is ready')

recv_time = 0
first_time = 0
counter = 1

def handle_client(client_socket):
    global recv_time, counter, first_time
    try:
        while True:
            Rec_message = client_socket.recv(65535)
            if not Rec_message:
                print("Client disconnected. Shutting down server.")
                client_socket.close()
            else:
                # message decode
                Rec_message = Rec_message.decode('utf-8')
                # temp = Rec_message.split()
                # calulate the Pocket_duration
                trans_time_next = time.time()
                Pocket_duration = (trans_time_next - recv_time) * 1000 
                if recv_time == 0:
                    first_time = trans_time_next
                    Pocket_duration = 0
                print(Rec_message)
                # if counter % 10000 == 0:
                # print(str(format(counter, '3d')) + '=>' + Rec_message + ' |  Packet duration = ' + str(format(Pocket_duration, '1.5f')) + ' ms, ' + 'total time = ' + str(format((trans_time_next - first_time)*1000, '1.5f')) + ' ms')

                # client_socket.send(b"ACK!")

                # print(client_socket.getpeername())
                # 

                recv_time = trans_time_next
                counter += 1
    except OSError as e:
        print(f"Socket error: {e}")
        client_socket.close()



def main():
    receiver_ip = '192.168.88.250'
    receiver_port = 5500

    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # create an SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="../tobby/server.crt", keyfile="../tobby/server.key")

    # bind the socket to the address and port
    server.bind((receiver_ip, receiver_port))
    server.listen(5)
    print(f"Listening on {receiver_ip}:{receiver_port}")

    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")

    # wrap the client socket with the SSL context
    ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
    handle_client(ssl_client_socket)

if __name__ == "__main__":
    main()
