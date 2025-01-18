from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
# from Infrastructure.Models.video_metadata_storage_bucket_link_model import VideoMetadataStorageBucketLinkModel

class StorageBucketModel(SQLModel, table=True):
    """
    Represents a storage bucket entity.
    """
    uuid: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to link video metadata
    # video_metadata_links: List[VideoMetadataStorageBucketLinkModel] = Relationship(back_populates="storage_bucket")

