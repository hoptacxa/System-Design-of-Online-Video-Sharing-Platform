from fastapi.testclient import TestClient
from Presentation.Routes.main import app
import socketio

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)
cid = f"Qm{'1' * 44}"

def test_dispatch_from_gateway():
    response = client.get(f"/command/get/{cid}/test.txt")
    
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers, "Missing 'Content-Disposition' header"
    assert "attachment" in response.headers["Content-Disposition"], "Response is not a file download"
    assert "test.txt" in response.headers["Content-Disposition"], "Downloaded file name mismatch"

    print("Test dispatch from gateway")

def test_dispatch_from_gateway_and_broadcast():
    responder_registration = {
        "peerId": "peer2",
        "peerAddress": "/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer",
        "storageCapacity": 10,
        "accessKeyId": "user1",
        "accessSecretKey": "secret1",
    }
    sio_responder = socketio.Client()
    @sio_responder.on('request')
    def handle_request(data):
        print("Responder nhận được request:", data)
        uuid_val = data.get('uuid')
        sio_responder.emit('response', {"uuid": uuid_val, "Body": "H4sIADy7kGcAAwvJyCxWKC4tKMgvKilWSMsvUihJLS4pBgAf9235FwAAAA=="})

    sio_responder.connect('http://127.0.0.1:3000', {}, responder_registration)
    # 
    dispatch_from_gateway_and_broadcast_with_external_running_peer()
    sio_responder.disconnect()

def test_dispatch_from_gateway_and_broadcast_with_external_running_peer():
    dispatch_from_gateway_and_broadcast_with_external_running_peer()

def dispatch_from_gateway_and_broadcast_with_external_running_peer():
    response = client.get(f"/command/get/{cid}/test.txt")
    
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers, "Missing 'Content-Disposition' header"
    assert "attachment" in response.headers["Content-Disposition"], "Response is not a file download"
    assert "test.txt" in response.headers["Content-Disposition"], "Downloaded file name mismatch"

    print("Test dispatch from gateway")

def test_pull_from_gateway():
    response = client.get("/command/pull/QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqA/segment_001.ts")
    
    assert response.status_code == 200
    assert "segment_001.ts" in response.headers["Content-Disposition"], "Downloaded file name mismatch"

def test_naming_service():
    response = client.get("/command/get/QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqA/metadata/names/0/n")
    assert response.status_code == 200

    response = client.get("/command/get/n/output.m3u8")
    assert response.status_code == 200
    assert "output.m3u8" in response.headers["Content-Disposition"], "Downloaded file name mismatch"
