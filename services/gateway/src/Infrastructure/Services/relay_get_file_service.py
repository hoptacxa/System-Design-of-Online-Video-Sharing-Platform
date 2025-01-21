import socketio
import uuid
import time

sio_requester = socketio.Client()

# Đăng ký thông tin peer
requester_registration = {
    "peerId": "peer1",
    "peerAddress": "/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer",
    "storageCapacity": 10,
    "accessKeyId": "user1",
    "accessSecretKey": "secret1",
}

# Hàm xử lý của requester khi nhận được response
@sio_requester.on('response')
def handle_response(response):
    print("Requester nhận được response:", response)
    assert response.get("Body") == "Response received", "Response không đúng!"
    print("Test hoàn tất!")

# Hàm xử lý lỗi cho requester
@sio_requester.on('error')
def handle_error(error):
    print(f"Lỗi xảy ra: {error}")
    raise Exception(f"Unexpected error: {error}")

class RelayGetFileService:
    def get_file_contents(self, provider_peer_uuid: str, file_key: str) -> bytes:
        sio_requester.connect('http://127.0.0.1:3000', {}, requester_registration)
        request_data = {
            "peerId": "peer1",
            "to": "peer2",
            "payload": {
                "data": {
                    file_key,
                }
            },
            "uuid": str(uuid.uuid4())
        }
        print("Requester gửi request:", request_data)
        sio_requester.emit('request', request_data)
