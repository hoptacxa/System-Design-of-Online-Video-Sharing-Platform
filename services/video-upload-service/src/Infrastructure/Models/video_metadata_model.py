from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
# from Infrastructure.Models.video_metadata_storage_bucket_link_model import VideoMetadataStorageBucketLinkModel

class VideoMetadataModel(SQLModel, table=True):
    """
    Represents a video metadata entity.
    """
    __tablename__ = "video_metadata"

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to link storage buckets
    # storage_bucket_links: List[VideoMetadataStorageBucketLinkModel] = Relationship(back_populates="video_metadata")

