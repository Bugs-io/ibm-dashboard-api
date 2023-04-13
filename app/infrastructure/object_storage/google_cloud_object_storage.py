from app.infrastructure.object_storage.object_storage import ObjectStorage
from google.cloud import storage


class GoogleCloudStorage(ObjectStorage):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = storage.Client()

    def _get_bucket(self):
        return self.client.get_bucket(self.bucket_name)

    def upload_internal_raw_dataset(self, file_name: str, file_content: bytes):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(file_content)

        return blob.public_url
