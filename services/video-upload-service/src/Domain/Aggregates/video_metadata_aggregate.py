from typing import List
from uuid import UUID
from Domain.Entities import video_metadata as VideoMetadata, storage_bucket as StorageBucket
from Domain.ValueObjects import duration as Duration, resolution as Resolution, title as Title, description as Description, file_key as FileKey


from Domain.ValueObjects.file_key import FileKey

class VideoMetadataAggregate:
    """
    Represents the domain model for Video Metadata, including file key,
    storage buckets, duration, resolution, title, and description.
    """
    def __init__(
        self,
        uuid: UUID,
        title: Title,
        description: Description,
        file_key: FileKey,
        duration: Duration,
        resolution: Resolution,
        user_id: int,
        # storage_buckets: List[StorageBucket],
    ):
        print("VideoMetadataAggregate")
    #     if not isinstance(uuid, UUID):
    #         raise ValueError("The uuid must be a valid UUID instance.")
    #     if not isinstance(title, Title):
    #         raise ValueError("The title must be a valid Title instance.")
    #     if not isinstance(description, Description):
    #         raise ValueError("The description must be a valid Description instance.")
    #     if not isinstance(file_key, FileKey):
    #         raise ValueError("The file_key must be a valid FileKey instance.")
    #     if not isinstance(duration, Duration):
    #         raise ValueError("The duration must be a valid Duration instance.")
    #     if not isinstance(resolution, Resolution):
    #         raise ValueError("The resolution must be a valid Resolution instance.")
    #     if not isinstance(storage_buckets, list) or any(
    #         not isinstance(bucket, StorageBucket) for bucket in storage_buckets
    #     ):
    #         raise ValueError("Storage buckets must be a list of StorageBucket instances.")

        self.uuid = uuid
        self.title = title
        self.description = description
        self.file_key = file_key
        self.duration = duration
        self.resolution = resolution
        self.user_id = user_id
        # self._storage_buckets = storage_buckets

    # @property
    # def storage_buckets(self) -> List[StorageBucket]:
    #     """
    #     Returns the associated storage buckets.
    #     """
    #     return self._storage_buckets

    # @storage_buckets.setter
    # def storage_buckets(self, buckets: List[StorageBucket]):
    #     """
    #     Sets the associated storage buckets, ensuring validation if necessary.
    #     """
    #     if not isinstance(buckets, list):
    #         raise ValueError("Storage buckets must be a list of StorageBucket instances.")
    #     for bucket in buckets:
    #         if not isinstance(bucket, StorageBucket):
    #             raise ValueError(f"Invalid storage bucket type: {type(bucket)}")
    #     self._storage_buckets = buckets

    # def update_entity(self, entity: VideoMetadata):
    #     """
    #     Updates the given persistence entity with the current aggregate's data.
    #     """
    #     entity.uuid = self.uuid
    #     entity.title = self.title
    #     entity.description = self.description
    #     entity.file_key = self.file_key
    #     entity.duration = self.duration
    #     entity.resolution = self.resolution

    # @staticmethod
    # def reconstitute(
    #     entity: VideoMetadata,
    #     storage_buckets: List[StorageBucket],
    # ) -> "VideoMetadataAggregate":
    #     """
    #     Reconstitutes a VideoMetadataAggregate from a persistence entity and related storage buckets.
    #     """
    #     if not isinstance(entity, VideoMetadata):
    #         raise ValueError("The entity must be an instance of VideoMetadata.")

    #     if not isinstance(storage_buckets, list):
    #         raise ValueError("Storage buckets must be a list.")
    #     for bucket in storage_buckets:
    #         if not isinstance(bucket, StorageBucket):
    #             raise ValueError(f"Invalid storage bucket type: {type(bucket)}")

    #     return VideoMetadataAggregate(
    #         uuid=entity.uuid,
    #         title=entity.title,
    #         description=entity.description,
    #         file_key=entity.file_key,
    #         duration=entity.duration,
    #         resolution=entity.resolution,
    #         storage_buckets=storage_buckets,
    #     )
