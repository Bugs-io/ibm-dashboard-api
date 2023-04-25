from app.domain.datasets import InternalDataset
from uuid import UUID
from typing import List


class InternalDatasetRepository:
    def save(self, internal_dataset: InternalDataset) -> None:
        pass

    def get_by_id(self, internal_dataset_id: UUID) -> InternalDataset:
        pass

    def get_by_processed_file_path(
            self,
            processed_file_path: str
    ) -> InternalDataset:
        pass

    def get_by_raw_file_path(
            self,
            raw_file_path: str
    ) -> InternalDataset:
        pass

    def get_active_file(self) -> InternalDataset | None:
        pass

    def get_all_files(self) -> List[InternalDataset]:
        pass
