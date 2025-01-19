from fastapi import Depends
from Application.Commands.broadcast_command import BroadcastCommand
from Infrastructure.Repositories.node_read_repository import NodeReadRepository
from Domain.ValueObjects.cid import Cid

class BroadcastCommandHandler:
    def __init__(
        self,
        node_read_repository: NodeReadRepository = Depends()
    ):
        self.node_read_repository = node_read_repository

    def handle(self, command: BroadcastCommand) -> dict:
        node = self.node_read_repository.get_node_by_cid(Cid(command.cid))
        print(f"The node is broadcasting request for CID {command.cid}...")
        
        return node

