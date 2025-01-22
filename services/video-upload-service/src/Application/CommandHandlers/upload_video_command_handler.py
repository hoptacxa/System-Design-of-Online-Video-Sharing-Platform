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
from ..Services.video_processing_service import VideoProcessingService
from pathlib import Path

class UploadVideoCommandHandler:
    def __init__(
        self,
        write_repository: VideoMetadataWriteRepository = Depends(SqlVideoMetadataWriteRepository),
        file_upload_service: FileUploadService = Depends(S3FileUploadService),
        video_processing_service: VideoProcessingService = Depends(),
        database_engine: DatabaseEngine = Depends()
    ):
        self._write_repository = write_repository
        self.database_engine = database_engine
        self.file_upload_service = file_upload_service
        self.video_processing_service = video_processing_service

    def handle(self, command: UploadVideoCommand):
        cid = "QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqA"
        # Delegate the creation of video metadata to the aggregate.
        video_file = command.video_file
        # Process the video
        output_dir = "/tmp/segments"
        playlist_path = self.video_processing_service.generate_hls_output(input_file=video_file.read(), output_dir=output_dir)

        # Upload the segments and playlist
        uploaded_files = []
        for file_path in Path(output_dir).iterdir():
            if file_path.is_file():
                file_key = f"{cid}/{file_path.name}"
                self.file_upload_service.upload_file(
                    file_contents=file_path.read_bytes(),
                    file_key=file_key
                )
                uploaded_files.append(file_key)

        public_playlist_url = f"{command.file_key}/output.m3u8"

        public_url = self.file_upload_service.upload_file(
            file_contents=video_file,
            file_key=command.file_key
        )
        new_video_metadata = VideoMetadataAggregate(
            uuid=command.uuid,
            user_uuid=command.user_uuid,
            title=command.title,
            description=command.description,
            file_key=public_playlist_url,
            duration=command.duration,
            resolution=command.resolution,
            public_url=public_url
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
            "uuid": new_video_metadata.uuid,
            "public_url": new_video_metadata.public_url
        }
