from typing import Optional
from sqlmodel import Session, select, delete
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate as VideoMetadataAggregate
from Infrastructure.Models.storage_bucket_model import StorageBucketModel as StorageBucket
from Infrastructure.Models.video_metadata_model import VideoMetadataModel as VideoMetadata
from Infrastructure.Models.video_metadata_storage_bucket_link_model import VideoMetadataStorageBucketLinkModel as VideoMetadataStorageBucketLink

class VideoMetadataRepository:
    """
    Repository for managing video uploads, explicitly handling VideoMetadataStorageBucketLink persistence.
    """

    def save(self, aggregate: VideoMetadataAggregate, session: Session) -> VideoMetadataAggregate:
        """
        Saves a VideoMetadataAggregate to the database, explicitly persisting VideoMetadataStorageBucketLink relationships.
        """
        try:
            entity = aggregate.to_entity()

            session.add(entity)

            for bucket in aggregate.storage_buckets:
                bucket_entity = session.get(StorageBucket, bucket.id)
                if bucket_entity:
                    link = VideoMetadataStorageBucketLink(
                        video_metadata_id=entity.id, storage_bucket_id=bucket_entity.id
                    )
                    session.add(link)

            session.commit()
            session.refresh(entity)

            return VideoMetadataAggregate.from_entity(entity)
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error saving video upload: {str(e)}")

    def update(self, aggregate: VideoMetadataAggregate, session: Session) -> Optional[VideoMetadataAggregate]:
        """
        Updates a VideoMetadataAggregate in the database, including VideoMetadataStorageBucketLink relationships.
        """
        try:
            # Retrieve the existing entity
            entity = session.get(VideoMetadata, aggregate.id)
            if not entity:
                return None

            # Update entity attributes
            aggregate.update_entity(entity)
            # Update links
            session.exec(
                delete(VideoMetadataStorageBucketLink).where(VideoMetadataStorageBucketLink.video_metadata_id == entity.id)
            )
            for bucket in aggregate.storage_buckets:
                session.add(VideoMetadataStorageBucketLink(video_metadata_id=entity.id, storage_bucket_id=bucket.id))

            # Commit updates
            session.commit()
            session.refresh(entity)

            # Map back to aggregate
            return VideoMetadataAggregate.from_entity(entity)
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error updating video upload: {str(e)}")

    def delete(self, video_id: int, session: Session) -> bool:
        """
        Deletes a VideoMetadata and its associated VideoMetadataStorageBucketLink relationships.
        """
        try:
            entity = session.get(VideoMetadata, video_id)
            if not entity:
                return False

            # Delete relationships in the association table
            session.exec(
                delete(VideoMetadataStorageBucketLink).where(VideoMetadataStorageBucketLink.video_metadata_id == video_id)
            )

            # Delete the video entity
            session.delete(entity)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error deleting video upload: {str(e)}")

    def get_by_id(self, video_id: int, session: Session) -> Optional[VideoMetadataAggregate]:
        """
        Retrieves a VideoMetadataAggregate by ID, explicitly including VideoMetadataStorageBucketLink relationships.
        """
        try:
            # Retrieve the entity
            entity = session.get(VideoMetadata, video_id)
            if not entity:
                return None

            # Retrieve linked storage buckets
            links = session.exec(
                select(VideoMetadataStorageBucketLink).where(VideoMetadataStorageBucketLink.video_metadata_id == video_id)
            ).all()
            bucket_ids = [link.storage_bucket_id for link in links]
            buckets = session.exec(select(StorageBucket).where(StorageBucket.id.in_(bucket_ids))).all()

            # Attach buckets to the aggregate
            aggregate = VideoMetadataAggregate.from_entity(entity)
            aggregate.storage_buckets = buckets

            return aggregate
        except Exception as e:
            raise RuntimeError(f"Error retrieving video upload: {str(e)}")
