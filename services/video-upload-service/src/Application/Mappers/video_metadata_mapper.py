from typing import List
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
# from Infrastructure.Models.storage_bucket_model import StorageBucketModel as StorageBucket
# from Infrastructure.Models.video_metadata_model import VideoMetadataModel as VideoMetadata
from Domain.Entities.video_metadata import VideoMetadata
from Domain.Entities.storage_bucket import StorageBucket

class VideoMetadataMapper:
    """
    Mapper class for transforming between VideoMetadataAggregate and persistence entities.
    """

    @staticmethod
    def to_entity(aggregate: VideoMetadataAggregate) -> VideoMetadata:
        """Convert VideoMetadataAggregate to VideoMetadata entity."""
        entity = VideoMetadata(
            uuid=aggregate.uuid,
            user_uuid=aggregate.user_uuid,
            title=aggregate.title,
            description=aggregate.description,
            file_key=aggregate.file_key,
            duration=aggregate.duration,
            resolution=aggregate.resolution,
            public_url=aggregate.public_url
        )
        return entity

    @staticmethod
    def from_entity(entity: VideoMetadata, buckets: List[StorageBucket]) -> VideoMetadataAggregate:
        """Convert VideoMetadata entity and associated buckets to VideoMetadataAggregate."""

        aggregate = VideoMetadataAggregate(
            uuid=entity.uuid,
            title=entity.title,
            user_uuid=entity.user_uuid,
            file_key=entity.file_key,
            duration=entity.duration,
            resolution=entity.resolution,
            public_url=entity.public_url,
            description=entity.description,
        )

        return aggregate
