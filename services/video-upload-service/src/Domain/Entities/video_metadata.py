from dataclasses import dataclass
from Domain.ValueObjects import duration as Duration, resolution as Resolution, title as Title, description as Description, file_key as FileKey
from uuid import UUID

@dataclass
class VideoMetadata:
    uuid: UUID
    user_uuid: UUID
    title: Title
    description: Description
    file_key: FileKey
    duration: Duration
    resolution: Resolution
