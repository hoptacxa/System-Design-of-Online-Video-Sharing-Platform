from Application.Commands.download_command import DownloadCommand
from Application.Commands.broadcast_command import BroadcastCommand
from Infrastructure.Services.s3_get_file_service import S3GetFileService
from Application.CommandHandlers.broadcast_command_handler import BroadcastCommandHandler
from fastapi import Depends

class DownloadCommandHandler:

    def __init__(
        self,
        broadcast_command_handler: BroadcastCommandHandler = Depends(),
        s3_get_file_service: S3GetFileService = Depends()
    ):
        self.s3_get_file_service = s3_get_file_service
        self.broadcast_command_handler = broadcast_command_handler

    def handle(self, command: DownloadCommand) -> bytes:
        file_contents = self.s3_get_file_service.get_file_contents(command.cid)
        if file_contents is None:
            broadcast_command = BroadcastCommand(
                cid=command.cid
            )
            return self.broadcast_command_handler.handle(broadcast_command)

        return file_contents
