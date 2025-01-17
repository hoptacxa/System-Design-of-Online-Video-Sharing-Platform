import pytest
from fastapi.testclient import TestClient
from Presentation.Routes.main import app
from io import BytesIO
from fastapi import UploadFile
from pathlib import Path

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)

# Test: successful video upload
def test_successful_video_upload():
    tmp_path = Path("/tmp")
    filename = tmp_path / "test.mp4"
    # write a binary file to test the video upload
    filename.write_bytes(b"<file content>")
    with filename.open("rb") as file:
        response = client.post(
            "/upload_video/",
            json={"title": "test"},
            files={"files": ("test.mp4", file)},
        )
    
    # Assert the status code is 200 (OK)
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {"message": "Video uploaded successfully. Uploaded file: test.mp4"}
