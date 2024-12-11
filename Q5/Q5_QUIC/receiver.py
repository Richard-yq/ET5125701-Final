import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived
import time

recv_time = 0
first_time = 0
stream_length = 100

class ServerQuicProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        global recv_time, first_time
        trans_time_next = time.time()
        Pocket_duration = (trans_time_next - recv_time) * 1000 
        if recv_time == 0:
            first_time = trans_time_next
            Pocket_duration = 0
        if isinstance(event, HandshakeCompleted):
            max_bidi = self._quic._local_max_streams_bidi.value
            max_uni = self._quic._local_max_streams_uni.value
            print(f"Handshake completed with max_streams_bidi={max_bidi} and max_streams_uni={max_uni}")
            print("Handshake completed")
        elif isinstance(event, StreamDataReceived):
            # print(f"Received: {event.data.decode('utf-8')} | Duration: {Pocket_duration} ms | Total: {(trans_time_next - first_time) * 1000} ms\n")
            # print(f"Received: {event.data.decode('utf-8')}")
            print(f"{event.data.decode('utf-8')}")
            # print(f"FIN RECV")
            # self._quic.send_stream_data(event.stream_id, b"Hello from server!", end_stream=True)
            None

async def run_server():
    configuration = QuicConfiguration(is_client=False)
    configuration.max_stream_data = 65536
    configuration.max_datagram_frame_size = 1452
    configuration.initial_max_streams_bidi = stream_length  # Set max bidirectional streams
    configuration.initial_max_streams_uni = stream_length   # Set max unidirectional streams
    configuration.load_cert_chain(certfile="server.crt", keyfile="server.key")
    await serve("192.168.88.250", 4433, configuration=configuration, create_protocol=ServerQuicProtocol)
    print('伺服器已啟動，等待連線...')
    await asyncio.Future()

if __name__ == "__main__":
    print("Starting server...")
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("伺服器已關閉。")
