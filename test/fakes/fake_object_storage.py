from app.application.ports import ObjectStorage

class FakeObjectStorage(ObjectStorage):
    def __init__(self):
        self.files = {}

    def upload_raw_internal_dataset(self, file_name: str, file_content: bytes) -> str:
        self.files[file_name] = file_content
        return file_name

    def get_raw_internal_dataset(self, file_name: str) -> bytes:
        return self.files[file_name]

    def upload_processed_internal_dataset(self, file_name: str, file_content: bytes) -> str:
        self.files[file_name] = file_content
        return file_name

    def get_processed_internal_dataset(self, file_name: str) -> bytes:
        return self.files[file_name]

    def upload_raw_external_dataset(self, file_name: str, file_content: bytes) -> str:
        self.files[file_name] = file_content
        return file_name

    def get_raw_external_dataset(self, file_name: str) -> bytes:
        return self.files[file_name]

    def upload_processed_external_dataset(self, file_name: str, file_content: bytes) -> str:
        self.files[file_name] = file_content
        return file_name

    def get_processed_external_dataset(self, file_name: str) -> bytes:
        return self.files[file_name]
