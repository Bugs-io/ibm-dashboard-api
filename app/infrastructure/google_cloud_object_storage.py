from google.cloud import storage

from app.application.ports import ObjectStorage


class GoogleCloudStorage(ObjectStorage):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = storage.Client()

    def upload_file(self, file_path: str, file_content: bytes) -> str:
        bucket = self._get_bucket()
        blob = bucket.blob(file_path)
        blob.upload_from_string(file_content)
        return blob.public_url

    def _get_bucket(self):
        return self.client.get_bucket(self.bucket_name)

    def upload_raw_internal_dataset(self, file_name: str, file_content: bytes):
        directory = "raw_internal_datasets/"
        file_path = directory + file_name
        return self.upload_file(file_path, file_content)

    def upload_processed_internal_dataset(self,
                                          file_name: str,
                                          file_content: bytes):
        directory = "processed_internal_datasets/"
        file_path = directory + file_name
        return self.upload_file(file_path, file_content)
