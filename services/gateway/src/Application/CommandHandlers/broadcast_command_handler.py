from fastapi import Depends
from Application.Commands.broadcast_command import BroadcastCommand

class BroadcastCommandHandler:
    def __init__(
        self
    ):
        print("BroadcastCommandHandler init")

    def handle(self, command: BroadcastCommand) -> bytes:
        print(f"The node is broadcasting request for CID {command.cid}...")

