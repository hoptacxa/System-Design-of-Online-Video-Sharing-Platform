from Domain.ValueObjects.cid import Cid

class DownloadCommand:
    def __init__(
        self,
        cid: Cid
    ):
        self.cid = cid
