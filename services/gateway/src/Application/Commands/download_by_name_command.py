class DownloadByNameCommand:
    def __init__(
        self,
        name: str,
        filename: str
    ):
        self.filename = filename
        self.name = name
