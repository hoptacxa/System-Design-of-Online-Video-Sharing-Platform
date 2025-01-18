from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution

class UploadVideoCommand:
    """
    Command for uploading a video. It contains the necessary information
    to create a new VideoMetadata instance.
    """

    def __init__(
        self,
        uuid: str,
        title: str,
        description: str,
        duration: int,
        resolution: str,
        user_id: int,
        file_key: str
    ): # , thumbnail_key: str, duration: Duration, resolution: Resolution
        self.uuid = uuid
        self.title = title
        self.description = description
        self.duration = duration
        self.user_id = user_id
        self.file_key = file_key
        self.resolution = resolution
        # self.thumbnail_key = thumbnail_key
        # self.duration = duration
        # self.resolution = resolution
