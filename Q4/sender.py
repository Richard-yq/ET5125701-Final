import socket
import time
import threading
import queue

Proxy_IP = '192.168.88.15'
port1 = 5406
port2 = 5408
port3 = 5409

host = '192.168.88.24'


Number_of_packets = 20
message_queue = queue.Queue()


class PacketSender(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def run(self):
        message_queue.put((0))
        i = 0
        while True:
            try:
                N_ack = message_queue.get(timeout=0.0001)
                print(f"Retrive ACK Packet {N_ack}")
                i = N_ack + 1
                if N_ack == Number_of_packets:  
                    break
                message = "Packet " + str(format(i, '3d')) + " sended at t = " + str(format(time.time(), '.5f'))
                print(f"Send message to port {self.port} => {message}")
                
                self.oSocket.sendto(message.encode('utf-8'), (self.host, self.port))
                if Number_of_packets - 5 >= i:
                    message_queue.put((i))

                # ack = message_queue.get(timeout=0.0001)
                # print(f"ACK Packet {ack}")
                # message_queue.put((ack))
                
            except queue.Empty:
                message = "Packet " + str(format(i, '3d')) + " sended at t = " + str(format(time.time(), '.5f'))
                
                print(f"Send message to port {self.port} => {message}")
                
                self.oSocket.sendto(message.encode('utf-8'), (self.host, self.port))

            time.sleep(0.1)

class UDPReceiver(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.counter = 1
        self.running = True
        print(f'Started a UDP socket listening on port {port}')

    def run(self):
        while self.running:
            data, addr = self.socket.recvfrom(65535)
            message = data.decode('utf-8')
            temp = message.split()
            Npacket = int(temp[1])
            print(f"Receive Acknowledged Packet {Npacket}")
            if Number_of_packets - 5 < Npacket:
                message_queue.put((Npacket))
        

def main():
    oReceive = UDPReceiver(host, port3)
    oReceive.start()
    choose = input("Enter 1(port = 5406), 2(port = 5408), 3(port = 5406 and 5408) to start sending packets: ")
    if choose == '1':
        oSender = PacketSender(Proxy_IP, port1)
        oSender.start()
    elif choose == '2':
        oSender = PacketSender(Proxy_IP, port2)
        oSender.start()
    elif choose == '3':
        oSender1 = PacketSender(Proxy_IP, port1)
        oSender2 = PacketSender(Proxy_IP, port2)
        oSender1.start()
        oSender2.start()

    

if __name__ == "__main__":
    main()