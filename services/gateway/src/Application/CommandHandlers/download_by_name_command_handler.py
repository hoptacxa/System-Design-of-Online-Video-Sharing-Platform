from fastapi import Depends
from Application.Commands.download_command import DownloadCommand
from Application.Commands.download_by_name_command import DownloadByNameCommand
from Application.Commands.broadcast_command import BroadcastCommand
from Infrastructure.Services.s3_get_file_service import S3GetFileService
from Infrastructure.Services.local_cache_get_cid_service import LocalCacheGetCidService
from Infrastructure.Services.relay_get_cid_service import RelayGetCidService
from Application.CommandHandlers.broadcast_command_handler import BroadcastCommandHandler
from Application.CommandHandlers.download_command_handler import DownloadCommandHandler

class DownloadByNameCommandHandler:

    def __init__(
        self,
        broadcast_command_handler: BroadcastCommandHandler = Depends(),
        relay_get_cid_service: RelayGetCidService = Depends(),
        s3_get_file_service: S3GetFileService = Depends(),
        download_by_cid_command_handler: DownloadCommandHandler = Depends(),
    ):
        self.s3_get_file_service = s3_get_file_service
        self.local_cache_get_cid_service = LocalCacheGetCidService()
        self.broadcast_command_handler = broadcast_command_handler
        self.relay_get_cid_service = relay_get_cid_service
        self.download_by_cid_command_handler = download_by_cid_command_handler

    def handle(self, command: DownloadByNameCommand) -> bytes:
        cid = self.local_cache_get_cid_service.get_by_name(command.name)

        if cid is None:
            broadcast_command = BroadcastCommand(
                query=command.name
            )
            provider_peer = self.broadcast_command_handler.handle(broadcast_command)
            cid = self.relay_get_cid_service.get_cid_by_name(provider_peer, command.name)
            self.local_cache_get_cid_service.set(command.name, cid)

        if cid is None:
            raise Exception(f"CID not found for {command.name}")

        download_command = DownloadCommand(
            cid=cid,
            filename=command.filename
        )
        
        return self.download_by_cid_command_handler.handle(download_command)
