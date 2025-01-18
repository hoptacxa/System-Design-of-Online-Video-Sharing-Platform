from typing import Optional
from fastapi import Depends
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository
from Infrastructure.Repositories.inmemory_video_metadata_write_repository import get_video_metadata_write_repository
from Infrastructure.Repositories.sql_video_metadata_write_repository import SqlVideoMetadataWriteRepository, get_video_metadata_write_repository
from Domain.Entities.video_metadata import VideoMetadata
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Application.Commands.upload_video_command import UploadVideoCommand
from typing import Annotated
from sqlmodel import Session, create_engine

class UploadVideoCommandHandler:
    def __init__(
        self,
        write_repository: VideoMetadataWriteRepository = Annotated[VideoMetadataWriteRepository, Depends(get_video_metadata_write_repository)]
    ):
        self.engine = create_engine("sqlite:///database.db")
        self._write_repository = write_repository

    def handle(self, command: UploadVideoCommand):
        # Delegate the creation of video metadata to the aggregate.
        new_video_metadata = VideoMetadataAggregate(
            uuid=command.uuid,
            title=command.title,
            description=command.description,
            file_key=command.file_key,
            duration=command.duration,
            resolution=command.resolution,
        )
        # Open a database session
        with Session(self.engine) as session:
            try:
                # Save the aggregate
                saved_aggregate = self._write_repository.save(
                    aggregate=new_video_metadata,
                    session=session
                )
                
                # Print the saved aggregate
                # print(f"Saved video metadata with ID: {saved_aggregate.id}")
                # print(f"Storage buckets: {[bucket.name for bucket in saved_aggregate.storage_buckets]}")
            except RuntimeError as e:
                print(f"Failed to save video metadata: {str(e)}")
        # videoMetadataAggregate = self._write_repository.save(
        #     user_id=command.user_id,
        #     file_key=command.file_key,
        #     # thumbnail_key=command.thumbnail_key,
        #     # duration=command.duration,
        #     # resolution=command.resolution
        # )
        # raise NotImplementedError("Method not implemented")
        print("Saving video metadata")
        return {
            "uuid": "1234",
        }

def get_upload_video_command_handler() -> UploadVideoCommandHandler:
    return UploadVideoCommandHandler()
