from fastapi import FastAPI
from Presentation.Controllers.video_upload_controller import router as video_upload_router

app = FastAPI()
app.include_router(video_upload_router)
