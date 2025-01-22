from Domain.ValueObjects.duration import Duration
from Domain.ValueObjects.resolution import Resolution
from tempfile import SpooledTemporaryFile

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
        user_uuid: str,
        video_file: bytes,
        file_key: str
    ):
        self.uuid = uuid
        self.title = title
        self.description = description
        self.duration = duration
        self.user_uuid = user_uuid
        self.file_key = file_key
        self.resolution = resolution
        self.video_file: SpooledTemporaryFile = video_file
