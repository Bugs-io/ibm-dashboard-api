import magic
from kink import inject
from app.infrastructure.object_storage.object_storage import ObjectStorage
from app.application.errors import InvalidFileTypeError
from app.application.dtos import DatasetDTO
from app.domain.datasets import InternalDataset

SPREADSHEET_MIME_TYPES = [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]


@inject
class IBMDashboardService:
    def __init__(self, object_storage: ObjectStorage):
        self.object_storage = object_storage

    def _is_valid_file(self, file_content: bytes) -> bool:
        file_type = magic.from_buffer(file_content, mime=True)
        return file_type in SPREADSHEET_MIME_TYPES

    def upload_internal_dataset(self, file_name: str, file_content: bytes):
        if not self._is_valid_file(file_content):
            raise InvalidFileTypeError

        path = self.object_storage.upload_internal_raw_dataset(
                file_name,
                file_content
                )

        dataset = InternalDataset(name=file_name, path=path, is_active=True)

        # TODO: Save dataset to databse

        return DatasetDTO(name=dataset.name, path=dataset.path)
