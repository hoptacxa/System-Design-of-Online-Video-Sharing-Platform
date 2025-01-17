from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile
from fastapi import UploadFile, File

class UploadVideoRequest(BaseModel):
    # video_file: UploadFile = File(...),
    title: str
    description: Optional[str] = None
