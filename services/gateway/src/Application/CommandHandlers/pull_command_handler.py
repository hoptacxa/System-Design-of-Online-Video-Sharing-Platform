from Application.Commands.download_command import DownloadCommand
from Infrastructure.Services.s3_get_file_service import S3GetFileService
from Infrastructure.Services.local_cache_get_file_service import LocalCacheGetFileService
from fastapi import Depends

class PullCommandHandler:
    def __init__(
        self,
        s3_get_file_service: S3GetFileService = Depends(),
        local_cache_get_file_service: LocalCacheGetFileService = Depends()
    ):
        self.s3_get_file_service = s3_get_file_service
        self.local_cache_get_file_service = local_cache_get_file_service

    def handle(self, command: DownloadCommand) -> bytes:
        file_contents = self.local_cache_get_file_service.get_file_contents(f"{command.cid}/{command.filename}")

        if file_contents is None:
            file_contents = self.s3_get_file_service.get_file_contents(f"{command.cid}/{command.filename}")

        if file_contents is None:
            raise Exception(f"Could not download file with CID {command.cid}")

        return file_contents
