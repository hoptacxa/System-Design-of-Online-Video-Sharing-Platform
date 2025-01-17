# controllers/video_upload_controller.py

from fastapi import APIRouter, HTTPException
# from services.video_upload_service.src.Domain.Commands.upload_video_command import UploadVideoCommand
# from services.video_upload_service.src.Domain.CommandHandlers.upload_video_command_handler import UploadVideoCommandHandler
# from services.video_upload_service.src.Domain.ValueObjects.duration import Duration
# from services.video_upload_service.src.Domain.ValueObjects.resolution import Resolution
# from services.video_upload_service.src.Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
# from services.video_upload_service.src.Domain.Entities.video_metadata import VideoMetadata
from pydantic import BaseModel

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
class UploadVideoRequest(BaseModel):
    user_id: int
    resolution: str
    duration: int  # Duration in seconds
    file_key: str
    thumbnail_key: str

@router.post("/upload-video/")
async def upload_video(request: UploadVideoRequest):
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
