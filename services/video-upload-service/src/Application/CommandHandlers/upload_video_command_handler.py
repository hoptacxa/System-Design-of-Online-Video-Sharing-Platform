from typing import Optional
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository
from Domain.Entities.video_metadata import VideoMetadata

class UploadVideoCommandHandler:
    """
    Handler for processing the UploadVideoCommand. 
    This class contains the business logic for uploading a video.
    """

    def __init__(self, video_metadata_aggregate: VideoMetadataAggregate):
        self._video_metadata_aggregate = video_metadata_aggregate

    def handle(self, command: UploadVideoCommand) -> Optional[VideoMetadata]:
        """
        Handles the command to upload a video by creating new video metadata.

        :param command: The UploadVideoCommand object that contains the data.
        :return: The newly created VideoMetadata object if successful, otherwise None.
        """
        # Delegate the creation of video metadata to the aggregate.
        return self._video_metadata_aggregate.create_video_metadata(
            user_id=command.user_id,
            file_key=command.file_key,
            thumbnail_key=command.thumbnail_key,
            duration=command.duration,
            resolution=command.resolution
        )
