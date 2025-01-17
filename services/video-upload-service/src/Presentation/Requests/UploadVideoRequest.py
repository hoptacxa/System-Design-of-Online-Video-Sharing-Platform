# src/Presentation/Requests/UploadVideoRequest.py
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import UploadFile, File

class UploadVideoRequest(BaseModel):
    video_file: UploadFile = Field(..., description="The video file to upload")
    title: str = Field(..., max_length=100, description="The title of the video")
    description: Optional[str] = Field(None, max_length=500, description="Description of the video")

    class Config:
        schema_extra = {
            "example": {
                "video_file": "file (binary)",
                "title": "My Awesome Video",
                "description": "This is a cool video I just uploaded!"
            }
        }
