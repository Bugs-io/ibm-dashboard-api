class ObjectStorage:
    def upload_raw_internal_dataset(self, file_name: str, file_content: bytes):
        pass

    def upload_processed_internal_dataset(
            self,
            file_name: str,
            file_content: bytes):
        pass

    def download_internal_dataset_from_url(self, url: str, destination_file_path: str):
        pass
