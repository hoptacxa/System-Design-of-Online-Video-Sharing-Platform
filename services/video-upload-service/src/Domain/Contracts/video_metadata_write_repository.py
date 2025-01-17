from abc import ABC, abstractmethod
from Domain.Entities.video_metadata import VideoMetadata

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
        # pass
        print("Saving video metadata")

    @abstractmethod
    def update(self, video_metadata: VideoMetadata) -> None:
        """
        Updates the given video metadata.
        
        :param video_metadata: The VideoMetadata entity to update.
        """
        pass

def get_video_metadata_write_repository() -> VideoMetadataWriteRepository:
    return VideoMetadataWriteRepository()
