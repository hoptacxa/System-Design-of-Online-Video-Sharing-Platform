from Application.Contracts.file_upload_service import FileUploadService

class S3FileUploadService(FileUploadService):
    def upload_file(self, file_contents: bytes, file_key: str):
        print(f"Uploading file to S3 with key: {file_key}")
        return file_key
