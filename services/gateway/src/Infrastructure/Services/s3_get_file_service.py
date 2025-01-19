from boto3 import client
from botocore.exceptions import ClientError

class S3GetFileService:
    def get_file_contents(self, file_key: str) -> bytes:
        s3_endpoint = "http://localhost:9000"
        access_key="hao"
        secret_key="nghiemxuan"
        s3 = client("s3", endpoint_url=s3_endpoint, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        bucket_name = "video-upload-service"
        
        try:
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            return response["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                print(f"Error getting file from S3: {e.__class__.__name__}")
                raise e
        except Exception as e:
            print(f"Error getting file from S3: {e.__class__.__name__}")
            raise e
