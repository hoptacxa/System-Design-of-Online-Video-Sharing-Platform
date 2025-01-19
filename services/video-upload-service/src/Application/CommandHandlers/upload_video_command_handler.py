from fastapi import Depends
from Domain.Contracts.video_metadata_write_repository import VideoMetadataWriteRepository
from Infrastructure.Repositories.sql_video_metadata_write_repository import get_video_metadata_write_repository, SqlVideoMetadataWriteRepository
from Domain.Entities.video_metadata import VideoMetadata
from Domain.Aggregates.video_metadata_aggregate import VideoMetadataAggregate
from Application.Commands.upload_video_command import UploadVideoCommand
from typing import Annotated
from sqlmodel import Session, create_engine
from Infrastructure.Repositories.database_engine import DatabaseEngine
from Infrastructure.Services.s3_file_upload_service import S3FileUploadService
from Application.Contracts.file_upload_service import FileUploadService

class UploadVideoCommandHandler:
    def __init__(
        self,
        write_repository: VideoMetadataWriteRepository = Depends(SqlVideoMetadataWriteRepository),
        file_upload_service: FileUploadService = Depends(S3FileUploadService),
        database_engine: DatabaseEngine = Depends()
    ):
        self._write_repository = write_repository
        self.database_engine = database_engine
        self.file_upload_service = file_upload_service

    def handle(self, command: UploadVideoCommand):
        # Delegate the creation of video metadata to the aggregate.
        video_file = command.video_file
        video_file_length = len(video_file.read())
        self.file_upload_service.upload_file(
            file_contents=video_file,
            file_key=command.file_key
        )
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
