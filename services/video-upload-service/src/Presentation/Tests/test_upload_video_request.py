import pytest
from fastapi.testclient import TestClient
from Presentation.Routes.main import app
from io import BytesIO
from fastapi import UploadFile

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)

@pytest.fixture
def valid_upload_data():
    file = BytesIO(b"dummy video content")  # Tạo file video giả
    file.name = "test_video.mp4"  # Đặt tên cho file
    return UploadFile(file=file, filename="test_video.mp4")

# Test: successful video upload
def test_successful_video_upload(valid_upload_data):
    # Construct the request data as a dictionary
    # files = {"video_file": ("test_video.mp4", valid_upload_data.file, "video/mp4")}
    data = {"title": "My Test Video", "description": "A test video upload"}

    response = client.post("/upload_video/", data=data)
    
    # Assert the status code is 200 (OK)
    assert response.status_code == 200
    print(response.json())
