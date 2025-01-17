# controllers/video_upload_controller.py
from fastapi import UploadFile, File, Form

from fastapi import APIRouter, HTTPException, Depends
# from Domain.Commands.upload_video_command import UploadVideoCommand
# from Domain.CommandHandlers.upload_video_command_handler import UploadVideoCommandHandler
# from Domain.ValueObjects.duration import Duration
# from Domain.ValueObjects.resolution import Resolution
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

# Define Pydantic models for request validation

@router.post("/upload_video/")
async def upload_video(
    files: UploadFile,
):
    return {"message": "Video uploaded successfully. Uploaded file: " + files.filename}
    try:
        # Map the incoming request to a command
        resolution = Resolution(request.resolution)  # Validating resolution
        duration = Duration(request.duration)  # Validating duration

        command = UploadVideoCommand(
            user_id=request.user_id,
            file_key=request.file_key,
            thumbnail_key=request.thumbnail_key,
            duration=duration,
            resolution=resolution
        )
        
        # Handle the command through the handler
        video_metadata = upload_video_command_handler.handle(command)
        
        if video_metadata:
            return {"message": "Video uploaded successfully", "video_metadata": video_metadata}
        else:
            raise HTTPException(status_code=400, detail="Video upload failed")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle invalid input
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
