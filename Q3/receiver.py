import socket
import time
import threading
import queue
import datetime

host = '192.168.88.250'
port1 = 5405
port2 = 5407

sender_IP = '192.168.88.24'


message_queue = queue.Queue()

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
            try:
                data, addr = self.socket.recvfrom(65535)
                recv_time = time.time()
                
                try:
                    message = data.decode('utf-8')
                    message_queue.put((self.port, message, recv_time, self.counter))
                    self.counter += 1
                except UnicodeDecodeError:
                    print(f"Port {self.port} - Received invalid UTF-8 data")
                    
            except socket.error as e:
                if self.running:
                    print(f"Socket error on port {self.port}: {e}")

    def stop(self):
        self.running = False
        self.socket.close()

def main():
    receiver1 = UDPReceiver(host, port1)
    receiver2 = UDPReceiver(host, port2)
    
    receiver1.start()
    receiver2.start()

    try:
        while True:
            try:
                port, message, recv_time, counter = message_queue.get(timeout=0.1)
                current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                
                recv_time = time.time()
                temp = message.split()
                tran_time = float(temp[6])
                packet_delay = (recv_time - tran_time) * 1000

                if port == port2:
                    # print(f"\t \t \t \t \t \t \t \t \t \t[{current_time}] Port {port} - {str(format(counter, '3d'))}=> {message} => Latency = {str(format(packet_delay, '1.5f'))} ms")
                    print(f"\t \t \t \t \t \t \t \t \t \t \t Port {port} - {str(format(counter, '3d'))}=> {message} => Latency = {str(format(packet_delay, '1.5f'))} ms")
                else:
                    # print(f"[{current_time}] Port {port} - {str(format(counter, '3d'))}=> {message} => Latency = {str(format(packet_delay, '1.5f'))} ms")
                    print(f"Port {port} - {str(format(counter, '3d'))}=> {message} => Latency = {str(format(packet_delay, '1.5f'))} ms")
                message_queue.task_done()
            except queue.Empty:
                continue
            
    except KeyboardInterrupt:
        print("\nShutting down...")

        receiver1.stop()
        receiver2.stop()
        
        receiver1.join()
        receiver2.join()
        
        print("Program terminated")

if __name__ == "__main__":
    main()