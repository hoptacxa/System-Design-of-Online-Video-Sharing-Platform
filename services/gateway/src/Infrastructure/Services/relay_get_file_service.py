import socketio
import uuid
import time
import base64
import gzip
from io import BytesIO

# Đăng ký thông tin peer
requester_registration = {
    "peerId": "peer1",
    "peerAddress": "/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer",
    "storageCapacity": 10,
    "accessKeyId": "user1",
    "accessSecretKey": "secret1",
}


class RelayGetFileService:
    def __init__(self):
        # Khởi tạo Socket.IO client và các thuộc tính
        self.sio_requester = socketio.Client()
        self.response_map = {}

        # Đăng ký event handlers
        self.sio_requester.on('response', self.handle_response)
        self.sio_requester.on('error', self.handle_error)

        # Kết nối tới server
        try:
            self.sio_requester.connect('http://127.0.0.1:3000', {}, requester_registration, retry=True, wait_timeout=5)
        except Exception as e:
            print(f"Không thể kết nối tới server: {e}")
            raise e

    def handle_response(self, response):
        """Xử lý phản hồi từ server."""
        request_uuid = response.get("requestUuid")
        if request_uuid:
            self.response_map[request_uuid] = response
            print(f"Đã nhận được phản hồi cho UUID {request_uuid}")
        else:
            print("Phản hồi không có UUID!")

    def handle_error(self, error):
        """Xử lý lỗi từ server."""
        print(f"Lỗi xảy ra: {error}")
        raise Exception(f"Unexpected error: {error}")

    def get_file_contents(self, provider_peer_uuid: str, file_key: str) -> bytes:
        """Gửi yêu cầu lấy file và chờ phản hồi."""
        try:
            # Tạo UUID cho request này
            request_uuid = str(uuid.uuid4())

            request_data = {
                "peerId": "peer1",
                "to": "peer2",
                "payload": {
                    "data": {
                        "fileKey": file_key,
                    }
                },
                "uuid": request_uuid
            }
            self.sio_requester.emit('request', request_data)

            # Chờ phản hồi với timeout
            timeout = 8  # seconds
            start_time = time.time()
            while request_uuid not in self.response_map:
                if time.time() - start_time > timeout:
                    return None
                time.sleep(0.1)

            # Lấy response từ response_map
            response = self.response_map.pop(request_uuid)
            if response.get("Body"):
                compressed_data = base64.b64decode(response.get("Body"))
                # Decompress the GZIP data
                with gzip.GzipFile(fileobj=BytesIO(compressed_data)) as gzip_file:
                    decompressed_data = gzip_file.read()
                # Save or use the decompressed data

                return decompressed_data
            else:
                raise ValueError(f"Phản hồi không hợp lệ: {response}")

        except Exception as e:
            print(f"Error during file retrieval: {e}")
            
            raise e
            return None

    def close_connection(self):
        """Đóng kết nối Socket.IO."""
        self.sio_requester.disconnect()
        print("Requester đã ngắt kết nối với server!")
