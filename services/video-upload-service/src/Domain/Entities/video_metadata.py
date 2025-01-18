from dataclasses import dataclass
from Domain.ValueObjects import duration as Duration, resolution as Resolution, title as Title, description as Description, file_key as FileKey

@dataclass
class VideoMetadata:
    id: int
    user_id: int
    title: Title
    description: Description
    file_key: FileKey
    duration: Duration
    resolution: Resolution
