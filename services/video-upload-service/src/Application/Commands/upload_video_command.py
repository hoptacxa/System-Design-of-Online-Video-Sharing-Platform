from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution

class UploadVideoCommand:
    """
    Command for uploading a video. It contains the necessary information
    to create a new VideoMetadata instance.
    """

    def __init__(self, user_id: int, file_key: str, thumbnail_key: str, duration: Duration, resolution: Resolution):
        self.user_id = user_id
        self.file_key = file_key
        self.thumbnail_key = thumbnail_key
        self.duration = duration
        self.resolution = resolution
