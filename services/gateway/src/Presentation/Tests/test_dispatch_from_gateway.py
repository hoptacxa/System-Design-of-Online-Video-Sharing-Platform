from fastapi.testclient import TestClient
from Presentation.Routes.main import app

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)

def test_dispatch_from_gateway():
    response = client.get("/command/get?cid=cid1")
    
    print(response.json())
    assert response.status_code == 200
    assert response.content == b'"Hello, World!"'

    print("Test dispatch from gateway")
