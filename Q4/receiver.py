import socket
import time
import threading
import queue
import datetime
import zlib
import re
# import sys

host = '192.168.88.250'
port1 = 5405
port2 = 5407

sender_IP = '192.168.88.24'
sender_port = 5409

Max_of_packets = 20

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
                    message_queue.put((self.port, data, recv_time, self.counter))
                    self.counter += 1
                except UnicodeDecodeError:
                    print(f"Port {self.port} - Received invalid UTF-8 data")
                    
            except socket.error as e:
                if self.running:
                    print(f"Socket error on port {self.port}: {e}")

    def stop(self):
        self.running = False
        self.socket.close()


def Acknowledge(sender_IP, sender_port, message):
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Send {message} to {sender_IP}:{sender_port}")
    sender_socket.sendto(message.encode('utf-8'), (sender_IP, sender_port))
    sender_socket.close()


def display_progress_bar(received_packets, max_packets):
    progress = len(received_packets) / max_packets  # 計算進度百分比
    bar_length = 40  # 進度條的長度
    filled_length = int(bar_length * progress)
    
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percent = progress * 100
    print(f"\r[{bar}] {percent:.2f}% ({len(received_packets * 5000)}/{max_packets * 5000} packets)")
    # sys.stdout.flush()

def main():
    receiver1 = UDPReceiver(host, port1)
    receiver2 = UDPReceiver(host, port2)
    
    receiver1.start()
    receiver2.start()

    received_packets = []

    try:
        while True:
            try:
                port, comp_message, recv_time, counter = message_queue.get(timeout=0.0001)
                current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                
                # Calculate the total time of receiving
                if counter == 1:
                    Start_receiving_time = recv_time
                Total_receiving_time = recv_time - Start_receiving_time

                message = zlib.decompress(comp_message)
                packetN = message.decode('utf-8')
                # print(packetN)

                # print(f"\t \t \t \t \t \t \t \t \t \t[{current_time}] Port {port} - {str(format(counter, '3d'))}=> {message} => Latency = {str(format(packet_delay, '1.5f'))} ms")
                print(f"Port {port} - {str(format(counter, '3d'))} => Total Receiving Time = {str(format(Total_receiving_time, '1.2f'))} s")
                
                # Retrieve the data from the message

                match = re.match(r"Group (\d+) \{(.*?)\}", packetN)
                if match:
                    group = match.group(1)
                    packets = match.group(2).split(', ')
                    packets = packets[0].split(',')
                    if int(group) not in received_packets:
                        received_packets.append(int(group))
                        received_packets.sort()
                        print(f"Group: {group}")
                        print(f"Packets: {packets[0]} to {packets[len(packets) - 1]}")
                        # print(f"Progress of Received packets: {received_packets}")
                else:
                    print("Message format is incorrect")

                print(f"Progress of Received Group: {received_packets}")
                display_progress_bar(received_packets, Max_of_packets)
                

                Acknowledge(sender_IP, sender_port, f"Ack {group}")

                message_queue.task_done()
            except queue.Empty:
                # print("wait")
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