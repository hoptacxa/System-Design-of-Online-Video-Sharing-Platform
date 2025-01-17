from typing import List, Optional
from Domain.Entities.video_metadata import VideoMetadata
from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution
from Domain.Contracts.video_metadata_read_repository import VideoMetadataReadRepository

class InMemoryVideoMetadataReadRepository(VideoMetadataReadRepository):
    def __init__(self):
        self._video_metadata_store = {}  # Mock storage, using a dictionary keyed by video_id

    def get_by_id(self, video_id: int) -> Optional[VideoMetadata]:
        return self._video_metadata_store.get(video_id)

    def get_all_by_user(self, user_id: int) -> List[VideoMetadata]:
        return [video for video in self._video_metadata_store.values() if video.user_id == user_id]

    def get_by_resolution(self, resolution: Resolution) -> List[VideoMetadata]:
        return [video for video in self._video_metadata_store.values() if video.resolution.value == resolution.value]

    def get_by_duration_range(self, min_duration: Duration, max_duration: Duration) -> List[VideoMetadata]:
        return [video for video in self._video_metadata_store.values() if min_duration.value <= video.duration.value <= max_duration.value]

def get_video_metadata_read_repository() -> InMemoryVideoMetadataReadRepository:
    return InMemoryVideoMetadataReadRepository()
