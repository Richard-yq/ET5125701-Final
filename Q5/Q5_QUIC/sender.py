import asyncio
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived
import time

stream_length = 1
packet_length = 1000000
class ClientQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream_ids = []

    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            max_bidi = self._quic._local_max_streams_bidi.value
            max_uni = self._quic._local_max_streams_uni.value
            print(f"Handshake completed with max_streams_bidi={max_bidi} and max_streams_uni={max_uni}")
            for _ in range(stream_length):
                stream_id = self._quic.get_next_available_stream_id(is_unidirectional=True)
                self._stream_ids.append(stream_id)
                # print(f"Generated stream ID: {stream_id}")
            asyncio.create_task(self.send_data_on_streams())
                
        elif isinstance(event, StreamDataReceived):
            print(f"Received: {event.data.decode()}")

    async def send_data_on_streams(self):
        tasks = []
        count = 0
        for stream_id in self._stream_ids:
            # print("Sending data on stream", count+1, stream_id)
            tasks.append(asyncio.create_task(self.send_data(stream_id, count + 1)))
            count += 1
        await asyncio.gather(*tasks)

    async def send_data(self, stream_id, num):
        for i in range((num - 1)* int(packet_length/stream_length) + 1, num * int(packet_length/stream_length) + 1):
            message = f"Packet {i:6d}\n"
            # message = "Group " + str(num) + " {" + ",".join([f"Packet {j}" for j in range((num-1)*int(packet_length/stream_length)+1 , num*int(packet_length/stream_length)+1)]) + "}"
            self._quic.send_stream_data(stream_id, message.encode('utf-8'))
            # time.sleep(0.0005)
        self._quic.send_stream_data(stream_id, b"", end_stream=True)

async def send_data():
    configuration = QuicConfiguration(is_client=True)
    configuration.max_stream_data = 65536
    configuration.max_datagram_frame_size = 1452
    configuration.verify_mode = False
    configuration.initial_max_streams_bidi = stream_length  # Set max bidirectional streams
    configuration.initial_max_streams_uni = stream_length   # Set max unidirectional streams
    async with connect("192.168.88.250", 4433, configuration=configuration, create_protocol=ClientQuicProtocol) as protocol:
        await protocol.wait_closed()

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_data())