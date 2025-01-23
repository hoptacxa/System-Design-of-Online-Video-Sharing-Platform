from Application.Commands.download_command import DownloadCommand
from Infrastructure.Services.s3_get_file_service import S3GetFileService
from Infrastructure.Services.local_cache_get_file_service import LocalCacheGetFileService
from fastapi import Depends
import base64
import gzip
from io import BytesIO

class PullCommandHandler:
    def __init__(
        self,
        s3_get_file_service: S3GetFileService = Depends(),
    ):
        self.s3_get_file_service = s3_get_file_service
        self.local_cache_get_file_service = LocalCacheGetFileService()

    def handle(self, command: DownloadCommand) -> bytes:
        file_contents = self.local_cache_get_file_service.get_file_contents(f"{command.cid}/{command.filename}")

        if file_contents is None:
            file_contents = self.s3_get_file_service.get_file_contents(f"{command.cid}/{command.filename}")

        if file_contents is None:
            raise Exception(f"Could not download file with CID {command.cid}")

        # Compress the file with Gzip
        gzip_buffer = BytesIO()
        with gzip.GzipFile(fileobj=gzip_buffer, mode="wb") as gzip_file:
            gzip_file.write(file_contents)

        # Encode the Gzip-compressed content in Base64
        compressed_data = gzip_buffer.getvalue()
        base64_encoded_data = base64.b64encode(compressed_data)

        return base64_encoded_data
