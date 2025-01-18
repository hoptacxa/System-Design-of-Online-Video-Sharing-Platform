from typing import Optional
from fastapi import Depends
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository
from Infrastructure.Repositories.inmemory_video_metadata_write_repository import get_video_metadata_write_repository
from Domain.Entities.video_metadata import VideoMetadata
from Application.Commands.upload_video_command import UploadVideoCommand
from typing import Annotated

class UploadVideoCommandHandler:
    def __init__(self, write_repository: VideoMetadataWriteRepository = Annotated[VideoMetadataWriteRepository, Depends(get_video_metadata_write_repository)]):
        self._write_repository = write_repository

    def handle(self, command: UploadVideoCommand):
        # return 
        # Delegate the creation of video metadata to the aggregate.
        # VideoMetadataAggregate(self._write_repository)
        # videoMetadataAggregate = self._write_repository.save(
        #     user_id=command.user_id,
        #     file_key=command.file_key,
        #     # thumbnail_key=command.thumbnail_key,
        #     # duration=command.duration,
        #     # resolution=command.resolution
        # )
        # raise NotImplementedError("Method not implemented")
        print("Saving video metadata")
        return {
            "uuid": "1234",
        }

def get_upload_video_command_handler() -> UploadVideoCommandHandler:
    return UploadVideoCommandHandler()
