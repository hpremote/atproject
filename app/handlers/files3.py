import logging
from os import environ
from boto3 import client


logging.basicConfig(level=logging.INFO)


class FileHandler:
    def __init__(self):
        self.s3_client = client(
            's3',
            endpoint_url=environ.get("S3_STORAGE_URL"),
            aws_access_key_id=environ.get("S3_ACCESS_ID"),
            aws_secret_access_key=environ.get("S3_SECRET_KEY")
        )
        self.storage_url = environ.get("S3_STORAGE_URL")
        self.s3_bucket_name = environ.get("S3_BUCKET_NAME")
        logging.debug("----- Initialized S3 bucket client -----")

    def store_s3(self, file_obj, filename: str):
        response = self.s3_client.upload_fileobj(file_obj, self.s3_bucket_name, filename, ExtraArgs={'ACL': 'public-read'})
        url = f"{self.storage_url}/ufiles/{filename}"

        return {"url": url}


file_handler = FileHandler()
