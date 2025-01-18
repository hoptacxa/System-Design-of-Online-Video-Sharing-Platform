from fastapi import Depends
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository
from Infrastructure.Repositories.sql_video_metadata_write_repository import get_video_metadata_write_repository, SqlVideoMetadataWriteRepository
from Domain.Entities.video_metadata import VideoMetadata
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Application.Commands.upload_video_command import UploadVideoCommand
from typing import Annotated
from sqlmodel import Session, create_engine
from Infrastructure.Repositories.database_engine import DatabaseEngine

class UploadVideoCommandHandler:
    def __init__(
        self,
        write_repository: VideoMetadataWriteRepository = Depends(SqlVideoMetadataWriteRepository),
        database_engine: DatabaseEngine = Depends()
    ):
        self._write_repository = write_repository
        self.database_engine = database_engine

    def handle(self, command: UploadVideoCommand):
        # Delegate the creation of video metadata to the aggregate.
        new_video_metadata = VideoMetadataAggregate(
            uuid=command.uuid,
            user_uuid=command.user_uuid,
            title=command.title,
            description=command.description,
            file_key=command.file_key,
            duration=command.duration,
            resolution=command.resolution,
        )
        # Open a database session
        with Session(self.database_engine.engine) as session:
            # Save the aggregate
            self._write_repository.save(
                aggregate=new_video_metadata,
                session=session
            )
            
        print("Saving video metadata")
        return {
            "uuid": "1234",
        }
