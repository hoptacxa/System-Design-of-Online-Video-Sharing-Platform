from fastapi import FastAPI, File, UploadFile
from typing import List
from Presentation.Controllers.video_upload_controller import router as video_upload_router

app = FastAPI()
app.include_router(video_upload_router)
# @app.post("/upload_video/")
# async def upload_video(
#     files: UploadFile,
# ):
#     return {"message": "Video uploaded successfully. Uploaded file: " + files.filename}
