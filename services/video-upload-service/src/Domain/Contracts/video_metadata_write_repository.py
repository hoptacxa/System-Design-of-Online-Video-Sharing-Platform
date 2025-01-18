from abc import ABC, abstractmethod
from typing import Optional
from sqlmodel import Session


class VideoMetadataWriteRepository(ABC):
    """
    Interface defining the contract for writing video metadata to a data source.
    """

    @abstractmethod
    def save(self, aggregate: "VideoUploadAggregate", session: Session) -> "VideoUploadAggregate":
        """
        Save video metadata to the data source.

        Args:
            aggregate (VideoUploadAggregate): The aggregate containing video metadata.
            session (Session): The database session.

        Returns:
            VideoUploadAggregate: The saved aggregate.
        """
        pass

    @abstractmethod
    def update(self, aggregate: "VideoUploadAggregate", session: Session) -> Optional["VideoUploadAggregate"]:
        """
        Update video metadata in the data source.

        Args:
            aggregate (VideoUploadAggregate): The aggregate containing video metadata.
            session (Session): The database session.

        Returns:
            Optional[VideoUploadAggregate]: The updated aggregate or None if not found.
        """
        pass

    @abstractmethod
    def delete(self, video_id: int, session: Session) -> bool:
        """
        Delete video metadata from the data source.

        Args:
            video_id (int): The ID of the video to delete.
            session (Session): The database session.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_by_id(self, video_id: int, session: Session) -> Optional["VideoUploadAggregate"]:
        """
        Retrieve video metadata by ID.

        Args:
            video_id (int): The ID of the video to retrieve.
            session (Session): The database session.

        Returns:
            Optional[VideoUploadAggregate]: The retrieved aggregate or None if not found.
        """
        pass
