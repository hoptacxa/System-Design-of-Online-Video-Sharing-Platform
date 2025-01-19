from Application.Commands.download_command import DownloadCommand
from Infrastructure.Services.s3_get_file_service import S3GetFileService
from fastapi import Depends

class DownloadCommandHandler:

    def __init__(self, s3_get_file_service: S3GetFileService = Depends()):
        self.s3_get_file_service = s3_get_file_service

    def handle(self, command: DownloadCommand) -> bytes:
        file_contents = self.s3_get_file_service.get_file_contents(command.cid)

        return file_contents
