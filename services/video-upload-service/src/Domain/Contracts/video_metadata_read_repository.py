from abc import ABC, abstractmethod
from typing import List, Optional
from services.video_upload_service.src.Domain.ValueObjects.duration import Duration
from services.video_upload_service.src.Domain.ValueObjects.resolution import Resolution
from services.video_upload_service.src.Domain.Entities.video_metadata import VideoMetadata

class VideoMetadataReadRepository(ABC):
    """
    This interface defines the contract for reading video metadata from the data source.
    """

    @abstractmethod
    def get_by_id(self, video_id: int) -> Optional[VideoMetadata]:
        """
        Fetches the video metadata by the given video_id.
        
        :param video_id: The ID of the video whose metadata is to be fetched.
        :return: VideoMetadata object if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> List[VideoMetadata]:
        """
        Fetches all video metadata uploaded by a specific user.
        
        :param user_id: The ID of the user whose videos are to be fetched.
        :return: List of VideoMetadata objects.
        """
        pass

    @abstractmethod
    def get_by_resolution(self, resolution: Resolution) -> List[VideoMetadata]:
        """
        Fetches all video metadata with the given resolution.
        
        :param resolution: Resolution filter (e.g., "1080p", "4K").
        :return: List of VideoMetadata objects that match the resolution.
        """
        pass

    @abstractmethod
    def get_by_duration_range(self, min_duration: Duration, max_duration: Duration) -> List[VideoMetadata]:
        """
        Fetches video metadata within a specified duration range.
        
        :param min_duration: The minimum duration of videos to be fetched.
        :param max_duration: The maximum duration of videos to be fetched.
        :return: List of VideoMetadata objects that match the duration range.
        """
        pass