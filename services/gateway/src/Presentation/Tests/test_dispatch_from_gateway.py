from fastapi.testclient import TestClient
from Presentation.Routes.main import app

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)

def test_dispatch_from_gateway():
    response = client.post(
        "/dispatch/",
        data={}
    )
    assert response.status_code == 200
    assert response.json() == {}

    print("Test dispatch from gateway")
