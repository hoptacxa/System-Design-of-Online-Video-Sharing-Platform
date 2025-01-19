from boto3 import client

class S3GetFileService:
    def get_file_contents(self, file_key: str) -> bytes:
        print(f"Getting file from S3 with key: {file_key}")
        s3_endpoint = "http://localhost:9000"
        access_key="hao"
        secret_key="nghiemxuan"
        s3 = client("s3", endpoint_url=s3_endpoint, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        bucket_name = "video-upload-service"
        
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        return response["Body"].read()
