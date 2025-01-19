# controllers/video_upload_controller.py
from fastapi import UploadFile, File, Form
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends
from Application.Commands.upload_video_command import UploadVideoCommand
from Application.CommandHandlers.upload_video_command_handler import UploadVideoCommandHandler
from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution
# from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
# from Domain.Entities.video_metadata import VideoMetadata
# from Infrastructure.Repositories.inmemory_video_metadata_read_repository import InMemoryVideoMetadataReadRepository, get_video_metadata_read_repository
# from pydantic import BaseModel
from Presentation.Requests.UploadVideoRequest import UploadVideoRequest

# Initialize the router
router = APIRouter()

# Dependency Injection: Define the repositories and aggregate
# video_metadata_read_repository = InMemoryVideoMetadataReadRepository()
# video_metadata_write_repository = InMemoryVideoMetadataWriteRepository()

# video_metadata_aggregate = VideoMetadataAggregate(
#     read_repository=video_metadata_read_repository,
#     write_repository=video_metadata_write_repository
# )

# upload_video_command_handler = UploadVideoCommandHandler(video_metadata_aggregate)


@router.post("/upload_video/", response_model=dict)
async def upload_video(
    request: Annotated[UploadVideoRequest, Form()], 
    command_handler: UploadVideoCommandHandler = Depends()
):
    try:
        command = UploadVideoCommand(
            uuid=uuid4(),
            title=request.title,
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
