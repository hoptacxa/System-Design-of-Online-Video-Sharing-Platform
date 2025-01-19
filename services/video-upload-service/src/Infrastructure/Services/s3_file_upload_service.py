from Application.Contracts.file_upload_service import FileUploadService
from boto3 import client

class S3FileUploadService(FileUploadService):
    def upload_file(self, file_contents: bytes, file_key: str):
        print(f"Uploading file to S3 with key: {file_key}")
        s3_endpoint = "http://localhost:9000"
        access_key="hao"
        secret_key="nghiemxuan"
        s3 = client("s3", endpoint_url=s3_endpoint, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        bucket_name = "video-upload-service"
        bucket_exists = False
        for bucket in s3.list_buckets()["Buckets"]:
            if bucket["Name"] == bucket_name:
                bucket_exists = True
                break
        if not bucket_exists:
            s3.create_bucket(Bucket=bucket_name)
        s3.put_object(
            Body=file_contents,
            Bucket="video-upload-service",
            Key=file_key
        )
        return file_key
