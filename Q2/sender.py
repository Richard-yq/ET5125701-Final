import socket
import time
import threading

host = '192.168.88.15'
port1 = 5406
port2 = 5408

class PacketSender(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def run(self):
        for _ in range(1, 101):
            for i in range(1, 11):
                message = "Packet " + str(format(i, '3d')) + " sended at t = " + str(format(time.time(), '.5f'))
                
                print(f"Send message to port {self.port} => {message}")
                
                self.oSocket.sendto(message.encode('utf-8'), (self.host, self.port))
                
                time.sleep(0.1)

def main():
    choose = input("Enter 1(port = 5406), 2(port = 5408), 3(port = 5406 and 5408) to start sending packets: ")
    if choose == '1':
        oSender = PacketSender(host, port1)
        oSender.start()
    elif choose == '2':
        oSender = PacketSender(host, port2)
        oSender.start()
    elif choose == '3':
        oSender1 = PacketSender(host, port1)
        oSender2 = PacketSender(host, port2)
        oSender1.start()
        oSender2.start()


if __name__ == "__main__":
    main()