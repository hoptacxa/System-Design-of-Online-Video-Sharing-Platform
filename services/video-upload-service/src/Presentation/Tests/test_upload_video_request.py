import pytest
from fastapi.testclient import TestClient
from Presentation.Routes.main import app
from io import BytesIO
from fastapi import UploadFile
from pathlib import Path
from Infrastructure.Repositories.database_engine import DatabaseEngine

# Create a TestClient instance for testing FastAPI endpoints
client = TestClient(app)
database_engine = DatabaseEngine()
database_engine.create_db_and_tables()
app.dependency_overrides[DatabaseEngine] = lambda: database_engine

# Test: successful video upload
def test_successful_video_upload():
    filename = Path("./LwekZs3Sp8g.webm")
    # write a binary file to test the video upload
    with filename.open("rb") as file:
        response = client.post(
            "/upload_video/",
            data={
                "title": "LwekZs3Sp8g",
                "name": "LwekZs3Sp8g",
                "description": "test",
                "duration": 1,
                "resolution": "1080p",
                "file_key": "LwekZs3Sp8g.webm"
            },
            files={"video_file": ("test.mp4", file)},
        )
    
    # delete the file
    # filename.unlink()
    # Assert the status code is 200 (OK)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Video uploaded successfully"
    assert response.json()["video_metadata"]["public_url"] == "http://localhost:9000/video-upload-service/LwekZs3Sp8g.webm"
    
