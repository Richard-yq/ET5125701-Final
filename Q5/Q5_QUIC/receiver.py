import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
import os
receiver_ip = '192.168.88.250'
receiver_port = 5500

recv_time = 0
counter = 1

class MyQuicProtocol(QuicConnectionProtocol):
    async def stream_handler(self, stream_id: int, stream_data: asyncio.StreamReader):
        global recv_time, counter

        data = await stream_data.read()
        if not data:
            return

        message = data.decode('utf-8')
        temp = message.split()
        print(f"Received message: {message}")

        # 計算封包延遲時間
        trans_time_next = asyncio.get_event_loop().time()
        pocket_duration = (trans_time_next - recv_time) * 1000

        if recv_time == 0:
            pocket_duration = 0

        print(f'{counter:3d} => {message} | Packet duration = {pocket_duration:1.5f} ms')

        # 發送回應
        self._quic.send_stream_data(stream_id, b"ACK!")
        await self._quic.wait_for_ack()

        recv_time = trans_time_next
        counter += 1

async def main():
    # QUIC 配置
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile="//home//rapi//ET5125701-Final//Q5//Q5_QUIC//cert.pem", keyfile="//home//rapi//ET5125701-Final//Q5//Q5_QUIC//key.pem")

    # 啟動 QUIC 伺服器
    await serve(receiver_ip, receiver_port, configuration=configuration, create_protocol=MyQuicProtocol)

if __name__ == "__main__":
    asyncio.run(main())
