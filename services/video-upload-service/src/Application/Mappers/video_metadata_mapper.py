from typing import List
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Infrastructure.Models.storage_bucket_model import StorageBucketModel as StorageBucket
from Infrastructure.Models.video_metadata_model import VideoMetadataModel as VideoMetadata


class VideoMetadataMapper:
    """
    Mapper class for transforming between VideoMetadataAggregate and persistence entities.
    """

    @staticmethod
    def to_entity(aggregate: VideoMetadataAggregate) -> VideoMetadata:
        """Convert VideoMetadataAggregate to VideoMetadata entity."""
        entity = VideoMetadata(
            id=aggregate.id,
            title=aggregate.title,
            description=aggregate.description,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
        )
        return entity

    @staticmethod
    def from_entity(entity: VideoMetadata, buckets: List[StorageBucket]) -> VideoMetadataAggregate:
        """Convert VideoMetadata entity and associated buckets to VideoMetadataAggregate."""
        aggregate = VideoMetadataAggregate(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            storage_buckets=buckets,
        )
        return aggregate

