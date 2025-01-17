from dataclasses import dataclass
from services.video_upload_service.src.Domain.ValueObjects.duration import Duration
from services.video_upload_service.src.Domain.ValueObjects.resolution import Resolution

@dataclass
class VideoMetadata:
    id: int
    user_id: int
    file_key: str
    thumbnail_key: str
    duration: Duration
    resolution: Resolution
