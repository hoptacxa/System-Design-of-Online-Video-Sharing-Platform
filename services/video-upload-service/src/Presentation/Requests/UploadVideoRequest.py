from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File, Form
from typing import List

class UploadVideoRequest(BaseModel):
    video_file: UploadFile = File(description="Multiple files as bytes"),
    title: str
    name: str
    description: str
    file_key: str
    resolution: str
    duration: int
