from abc import ABC, abstractmethod
from typing import Optional
from sqlmodel import Session
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate


class VideoMetadataWriteRepository(ABC):
    """
    Interface defining the contract for writing video metadata to a data source.
    """

    @abstractmethod
    def save(self, aggregate: VideoMetadataAggregate, session: Session) -> VideoMetadataAggregate:
        """
        Persist a VideoMetadataAggregate in the database.
        """
        pass

    @abstractmethod
    def update(self, aggregate: VideoMetadataAggregate, session: Session) -> Optional[VideoMetadataAggregate]:
        """
        Update an existing VideoMetadataAggregate in the database.
        """
        pass

    @abstractmethod
    def delete(self, video_id: int, session: Session) -> bool:
        """
        Delete a VideoMetadataAggregate and associated relationships by ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, video_id: int, session: Session) -> Optional[VideoMetadataAggregate]:
        """
        Retrieve a VideoMetadataAggregate by ID, including related entities.
        """
        pass
