from abc import ABC, abstractmethod
from services.video_upload_service.src.Domain.Entities.video_metadata import VideoMetadata

class VideoMetadataWriteRepository(ABC):
    """
    This interface defines the contract for writing video metadata to the data source.
    """
    
    @abstractmethod
    def save(self, video_metadata: VideoMetadata) -> None:
        """
        Saves the given video metadata.
        
        :param video_metadata: The VideoMetadata entity to save.
        """
        pass

    @abstractmethod
    def update(self, video_metadata: VideoMetadata) -> None:
        """
        Updates the given video metadata.
        
        :param video_metadata: The VideoMetadata entity to update.
        """
        pass
