from typing import Optional
from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution
from Domain.Entities.video_metadata import VideoMetadata
from Domain.Contracts.video_metadata_read_repository import VideoMetadataReadRepository

class VideoMetadataAggregate:
    """
    The aggregate root for managing video metadata, enforcing business rules,
    and interacting with repositories for persistence.
    """

    def __init__(self, repository: VideoMetadataReadRepository):
        self._repository = repository

    def create_video_metadata(
        self,
        user_id: int,
        file_key: str,
        thumbnail_key: str,
        duration: Duration,
        resolution: Resolution
    ) -> VideoMetadata:
        """
        Creates a new VideoMetadata instance, ensuring that the business rules are respected.
        
        :param user_id: The ID of the user uploading the video.
        :param file_key: The key for the video file.
        :param thumbnail_key: The key for the thumbnail image.
        :param duration: The duration of the video.
        :param resolution: The resolution of the video.
        :return: A new VideoMetadata object.
        """
        # Create a new VideoMetadata entity
        video_metadata = VideoMetadata(
            id=self._generate_new_id(),
            user_id=user_id,
            file_key=file_key,
            thumbnail_key=thumbnail_key,
            duration=duration,
            resolution=resolution
        )
        
        # You might save it to the repository here (assuming repository has a save method)
        self._repository.save(video_metadata)
        
        return video_metadata

    def get_video_metadata(self, video_id: int) -> Optional[VideoMetadata]:
        """
        Fetches video metadata by its ID.
        
        :param video_id: The ID of the video.
        :return: The VideoMetadata if found, otherwise None.
        """
        return self._repository.get_by_id(video_id)

    def update_video_metadata(
        self,
        video_id: int,
        duration: Optional[Duration] = None,
        resolution: Optional[Resolution] = None
    ) -> Optional[VideoMetadata]:
        """
        Updates the video metadata attributes. Can be used to update duration or resolution.
        
        :param video_id: The ID of the video.
        :param duration: The new duration value (optional).
        :param resolution: The new resolution value (optional).
        :return: The updated VideoMetadata object if successful, otherwise None.
        """
        video_metadata = self._repository.get_by_id(video_id)
        
        if not video_metadata:
            return None
        
        # Apply updates
        if duration:
            video_metadata.duration = duration
        if resolution:
            video_metadata.resolution = resolution

        # Save the updated metadata (assuming repository has a save method)
        self._repository.save(video_metadata)

        return video_metadata

    def _generate_new_id(self) -> int:
        """
        Generates a new unique ID for the video metadata. This is a placeholder method;
        in a real application, you may use auto-increment in a database or a UUID.
        """
        return 12345  # This is a dummy value for demonstration.
