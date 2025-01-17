from dataclasses import dataclass
from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution

@dataclass
class VideoMetadata:
    id: int
    user_id: int
    file_key: str
    thumbnail_key: str
    duration: Duration
    resolution: Resolution
