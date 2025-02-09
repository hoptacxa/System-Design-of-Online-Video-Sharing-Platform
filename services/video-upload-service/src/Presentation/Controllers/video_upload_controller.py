# controllers/video_upload_controller.py
from fastapi import Form
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends
from Application.Commands.upload_video_command import UploadVideoCommand
from Application.CommandHandlers.upload_video_command_handler import UploadVideoCommandHandler
from Presentation.Requests.UploadVideoRequest import UploadVideoRequest

router = APIRouter()

@router.post("/upload_video/", response_model=dict)
async def upload_video(
    request: Annotated[UploadVideoRequest, Form()], 
    command_handler: UploadVideoCommandHandler = Depends()
):
    try:
        command = UploadVideoCommand(
            uuid=uuid4(),
            title=request.title,
            name=request.name,
            description=request.description,
            resolution=request.resolution,
            duration=request.duration,
            user_uuid=uuid4(),
            file_key=request.file_key,
            video_file=request.video_file.file
        )
        
        # Handle the command through the handler
        video_metadata = command_handler.handle(command)
        
        if video_metadata:
            return {"message": "Video uploaded successfully", "video_metadata": video_metadata}
        else:
            raise HTTPException(status_code=400, detail="Video upload failed")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle invalid input
    except Exception as e:
        print(e)
        trace = e.__traceback__
        while trace.tb_next:
            trace = trace.tb_next
            print(f"Caused by: {trace.tb_frame.f_code.co_name} in {trace.tb_frame.f_code.co_filename}:{trace.tb_lineno}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
