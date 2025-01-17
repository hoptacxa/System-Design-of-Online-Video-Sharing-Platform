from typing import Optional
from fastapi import Depends
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository, get_video_metadata_write_repository
from Domain.Entities.video_metadata import VideoMetadata
from Application.Commands.upload_video_command import UploadVideoCommand

class UploadVideoCommandHandler:
    """
    Handler for processing the UploadVideoCommand. 
    This class contains the business logic for uploading a video.
    """

    def __init__(self, write_repository: VideoMetadataWriteRepository = Depends(get_video_metadata_write_repository)):
        self._write_repository = write_repository

    def handle(self, command: UploadVideoCommand):
        """
        Handles the command to upload a video by creating new video metadata.

        :param command: The UploadVideoCommand object that contains the data.
        :return: The newly created VideoMetadata object if successful, otherwise None.
        """
        
        # return 
        # Delegate the creation of video metadata to the aggregate.
        # self._write_repository.save(
        #     user_id=command.user_id,
        #     file_key=command.file_key,
        #     # thumbnail_key=command.thumbnail_key,
        #     # duration=command.duration,
        #     # resolution=command.resolution
        # )
        print("Saving video metadata")

def get_upload_video_command_handler() -> UploadVideoCommandHandler:
    return UploadVideoCommandHandler()
