from abc import ABC, abstractmethod
class FileUploadService(ABC):
    @abstractmethod
    def upload_file(self, file_contents: bytes, file_key: str):
        pass
