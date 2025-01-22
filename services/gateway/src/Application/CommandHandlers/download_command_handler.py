from Application.Commands.download_command import DownloadCommand
from Application.Commands.broadcast_command import BroadcastCommand
from Infrastructure.Services.s3_get_file_service import S3GetFileService
from Infrastructure.Services.peer_get_file_service import PeerGetFileService
from Infrastructure.Services.relay_get_file_service import RelayGetFileService
from Application.CommandHandlers.broadcast_command_handler import BroadcastCommandHandler
from fastapi import Depends

class DownloadCommandHandler:

    def __init__(
        self,
        broadcast_command_handler: BroadcastCommandHandler = Depends(),
        peer_get_file_service: PeerGetFileService = Depends(),
        relay_get_file_service: RelayGetFileService = Depends(),
        s3_get_file_service: S3GetFileService = Depends()
    ):
        self.s3_get_file_service = s3_get_file_service
        self.broadcast_command_handler = broadcast_command_handler
        self.peer_get_file_service = peer_get_file_service
        self.relay_get_file_service = relay_get_file_service

    def handle(self, command: DownloadCommand) -> bytes:
        file_contents = self.s3_get_file_service.get_file_contents(command.cid)
        if file_contents is None:
            broadcast_command = BroadcastCommand(
                cid=command.cid
            )
            provider_peer = self.broadcast_command_handler.handle(broadcast_command)
            print(f"Node {provider_peer['uuid']} has data for CID {command.cid}")
            file_contents = self.peer_get_file_service.get_file_contents(provider_peer['uuid'], command.cid)

        if file_contents is None:
            file_contents = self.relay_get_file_service.get_file_contents(provider_peer['uuid'], f"{command.cid}/{command.filename}")

        if file_contents is None:
            raise Exception(f"Could not download file with CID {command.cid}")

        return file_contents
