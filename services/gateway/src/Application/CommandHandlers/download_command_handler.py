from Application.Commands.download_command import DownloadCommand

class DownloadCommandHandler:
    def handle(self, command: DownloadCommand) -> bytes:
        return b"Hello, World!"
