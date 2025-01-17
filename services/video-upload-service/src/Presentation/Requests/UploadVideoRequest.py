from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File, Form
from typing import List

class UploadVideoRequest(BaseModel):
    video_file: UploadFile = File(description="Multiple files as bytes"),
    # video_file: UploadFile = Form(...),
    # title: str = Form(...)
    title: str
