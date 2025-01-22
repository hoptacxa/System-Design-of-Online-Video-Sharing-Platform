class DownloadCommand:
    def __init__(
        self,
        cid: str,
        filename: str
    ):
        self.filename = filename
        self.cid = cid
