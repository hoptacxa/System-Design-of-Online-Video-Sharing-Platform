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
            user_id=aggregate.user_id,
            title=aggregate.title,
            description=aggregate.description,
            file_key=aggregate.file_key,
            duration=aggregate.duration,
            resolution=aggregate.resolution,
        )
        return entity

    @staticmethod
    def from_entity(entity: VideoMetadata, buckets: List[StorageBucket]) -> VideoMetadataAggregate:
        """Convert VideoMetadata entity and associated buckets to VideoMetadataAggregate."""
        raise NotImplementedError("Not implemented")
        # aggregate = VideoMetadataAggregate(
        #     uuid=entity.id,
        #     title=entity.title,
        #     description=entity.description,
        #     created_at=entity.created_at,
        #     updated_at=entity.updated_at,
        #     storage_buckets=buckets,
        # )
        return aggregate

