from fastapi.testclient import TestClient
from Presentation.Routes.main import app

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)

def test_dispatch_from_gateway():
    response = client.get("/command/get?cid=test.txt")
    
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers, "Missing 'Content-Disposition' header"
    assert "attachment" in response.headers["Content-Disposition"], "Response is not a file download"
    assert "test.txt" in response.headers["Content-Disposition"], "Downloaded file name mismatch"

    print("Test dispatch from gateway")

def test_dispatch_from_gateway_and_broadcast():
    cid = f"Qm{'1' * 44}"
    response = client.get(f"/command/get?cid={cid}")
    
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers, "Missing 'Content-Disposition' header"
    assert "attachment" in response.headers["Content-Disposition"], "Response is not a file download"
    assert "test.txt" in response.headers["Content-Disposition"], "Downloaded file name mismatch"

    print("Test dispatch from gateway")
