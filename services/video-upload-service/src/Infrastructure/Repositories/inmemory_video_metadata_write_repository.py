from Domain.Entities.video_metadata import VideoMetadata
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository

class InMemoryVideoMetadataWriteRepository(VideoMetadataWriteRepository):
    def __init__(self):
        self._video_metadata_store = {}

    def save(self, video_metadata: VideoMetadata) -> None:
        """Saves the given VideoMetadata to the in-memory store."""
        raise NotImplementedError("Method not implemented")
        # self._video_metadata_store[video_metadata.id] = video_metadata

    def update(self, video_metadata: VideoMetadata) -> None:
        """Updates the given VideoMetadata in the in-memory store."""
        if video_metadata.id in self._video_metadata_store:
            self._video_metadata_store[video_metadata.id] = video_metadata

def get_video_metadata_write_repository() -> VideoMetadataWriteRepository:
    return InMemoryVideoMetadataWriteRepository()
