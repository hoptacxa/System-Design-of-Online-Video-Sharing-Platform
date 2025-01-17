from typing import Optional
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository
from Domain.Entities.video_metadata import VideoMetadata
from Application.Commands.upload_video_command import UploadVideoCommand

class UploadVideoCommandHandler:
    """
    Handler for processing the UploadVideoCommand. 
    This class contains the business logic for uploading a video.
    """

    def handle(self, command: UploadVideoCommand) -> Optional[VideoMetadata]:
        """
        Handles the command to upload a video by creating new video metadata.

        :param command: The UploadVideoCommand object that contains the data.
        :return: The newly created VideoMetadata object if successful, otherwise None.
        """
        
        # return 
        # Delegate the creation of video metadata to the aggregate.
        return self._video_metadata_aggregate.create_video_metadata(
            user_id=command.user_id,
            file_key=command.file_key,
            # thumbnail_key=command.thumbnail_key,
            # duration=command.duration,
            # resolution=command.resolution
        )

def get_upload_video_command_handler() -> UploadVideoCommandHandler:
    return UploadVideoCommandHandler()
