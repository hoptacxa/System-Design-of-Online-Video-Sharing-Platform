from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File, Form

class UploadVideoRequest(BaseModel):
    video_file: UploadFile = Form(...),
    # title: str = Form(...)
    # description: Optional[str] = Form(None)
