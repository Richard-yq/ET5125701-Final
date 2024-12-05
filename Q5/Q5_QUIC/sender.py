import asyncio
import time
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted
from aioquic.asyncio.protocol import QuicConnectionProtocol

sender_host = '192.168.88.24'
sender_port = 5407
receiver_ip = '192.168.88.250'
receiver_port = 5500

# 設定QUIC配置，這裡需要TLS憑證
configuration = QuicConfiguration(is_client=True)
configuration.load_cert_chain(certfile="//home//rapi//ET5125701-Final//Q5//Q5_QUIC//cert.pem", keyfile="//home//rapi//ET5125701-Final//Q5//Q5_QUIC//key.pem")  # 載入憑證

class MyQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._handshake_complete = False
    
    def handshake_complete(self):
        """握手完成時觸發"""
        self._handshake_complete = True

async def send_packets():
    # 與QUIC伺服器建立連線
    async with connect(receiver_ip, receiver_port, configuration=configuration, create_protocol=MyQuicProtocol) as protocol:
        # 發送 10 個封包
        for i in range(1, 11):
            message = f"Packet {i:3d} sended at t = {time.time():.5f}"
            print(message)
            
            # 使用 QUIC 的流來發送資料
            protocol._quic.send_stream_data(0, message.encode('utf-8'))  # 發送資料流

            # 讓伺服器有時間回應
            await asyncio.sleep(0.1)
        
        # 等待回應
        await protocol._quic.wait_for_ack()
        print("Finished sending packets.")

# 事件循環執行
asyncio.run(send_packets())
