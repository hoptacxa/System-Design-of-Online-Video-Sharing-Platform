from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
# from Infrastructure.Models.video_metadata_model import VideoMetadataModel
# from Infrastructure.Models.storage_bucket_model import StorageBucketModel

class VideoMetadataStorageBucketLinkModel(SQLModel, table=True):
    """
    Represents the many-to-many link between VideoMetadataModel and StorageBucketModel.
    """
    video_metadata_id: int = Field()
    storage_bucket_id: int = Field()

    # Relationships
    # video_metadata: VideoMetadataModel = Relationship(back_populates="storage_bucket_links")
    # storage_bucket: StorageBucketModel = Relationship(back_populates="video_metadata_links")

