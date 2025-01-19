from typing import Optional, List
from sqlmodel import Session, select, delete
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Domain.Entities.video_metadata import VideoMetadata
from Infrastructure.Models.storage_bucket_model import StorageBucketModel
from Infrastructure.Models.video_metadata_model import VideoMetadataModel
# from Infrastructure.Models.video_metadata_storage_bucket_link_model import VideoMetadataStorageBucketLinkModel as VideoMetadataStorageBucketLink
from Application.Mappers.video_metadata_mapper import VideoMetadataMapper
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository

class SqlVideoMetadataWriteRepository(VideoMetadataWriteRepository):
    """
    Repository for managing video uploads, explicitly handling VideoMetadataStorageBucketLink persistence.
    """

    def save(self, aggregate: VideoMetadataAggregate, session: Session) -> VideoMetadataAggregate:
        """
        Saves a VideoMetadataAggregate to the database, explicitly persisting VideoMetadataStorageBucketLink relationships.
        """
        
        try:
            entity = VideoMetadataMapper.to_entity(aggregate)
            new_video_metadata = VideoMetadataModel(
                uuid=entity.uuid,
                user_uuid=entity.user_uuid,
                title=entity.title,
                description=entity.description,
                file_key=entity.file_key,
                duration=entity.duration,
                public_url=entity.public_url,
                resolution=entity.resolution
            )
            session.add(instance=new_video_metadata)

            # Persist bucket links
            # for bucket in aggregate.storage_buckets:
            #     bucket_entity = session.get(StorageBucket, bucket.uuid)
            #     if bucket_entity:
            #         link = VideoMetadataStorageBucketLink(
            #             video_metadata_id=entity.uuid, storage_bucket_id=bucket_entity.uuid
            #         )
            #         session.add(link)

            session.commit()
            session.refresh(new_video_metadata)

            return SqlVideoMetadataWriteRepository.to_aggregate(new_video_metadata)
        except Exception as e:
            session.rollback()
            print(e.__traceback__.tb_lineno)
            raise RuntimeError(f"Error saving video upload: {str(e)}")

    def to_aggregate(model: VideoMetadataModel) -> VideoMetadataAggregate:
        entity = SqlVideoMetadataWriteRepository.to_entity(model)
        return VideoMetadataMapper.from_entity(entity, [])

    def to_entity(model: VideoMetadataModel) -> VideoMetadata:
        return VideoMetadata(
            uuid=model.uuid,
            user_uuid=model.user_uuid,
            file_key=model.file_key,
            title=model.title,
            description=model.description,
            duration=model.duration,
            public_url=model.public_url,
            resolution=model.resolution
        )

    def update(self, aggregate: VideoMetadataAggregate, session: Session) -> Optional[VideoMetadataAggregate]:
        """
        Updates a VideoMetadataAggregate in the database, including VideoMetadataStorageBucketLink relationships.
        """
        try:
            entity = session.get(VideoMetadata, aggregate.uuid)
            if not entity:
                return None

            # Update the entity's fields
            updated_entity = VideoMetadataMapper.to_entity(aggregate)
            entity.title = updated_entity.title
            entity.description = updated_entity.description
            entity.updated_at = updated_entity.updated_at

            # Update bucket links
            session.exec(
                delete(VideoMetadataStorageBucketLink).where(VideoMetadataStorageBucketLink.video_metadata_id == entity.uuid)
            )
            for bucket in aggregate.storage_buckets:
                session.add(VideoMetadataStorageBucketLink(video_metadata_id=entity.uuid, storage_bucket_id=bucket.uuid))

            session.commit()
            session.refresh(entity)

            return VideoMetadataMapper.from_entity(entity, aggregate.storage_buckets)
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

            session.exec(
                delete(VideoMetadataStorageBucketLink).where(VideoMetadataStorageBucketLink.video_metadata_id == video_id)
            )
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
            entity = session.get(VideoMetadata, video_id)
            if not entity:
                return None

            # Retrieve linked storage buckets
            buckets = session.exec(
                select(StorageBucket)
                .join(VideoMetadataStorageBucketLink, StorageBucket.uuid == VideoMetadataStorageBucketLink.storage_bucket_id)
                .where(VideoMetadataStorageBucketLink.video_metadata_id == video_id)
            ).all()

            return VideoMetadataMapper.from_entity(entity, buckets)
        except Exception as e:
            raise RuntimeError(f"Error retrieving video upload: {str(e)}")


def get_video_metadata_write_repository() -> VideoMetadataWriteRepository:
    return SqlVideoMetadataWriteRepository()
