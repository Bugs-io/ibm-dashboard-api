from pony.orm import db_session, Database, PrimaryKey, Required, select
from app.application.ports import InternalDatasetRepository
from app.domain import InternalDataset
from datetime import datetime
from typing import List
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

db = Database()
db.bind(
        provider=os.getenv('DB_PROVIDER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME')
        )



class InternalDatasetModel(db.Entity):
    _table_ = "internal_datasets"
    internal_dataset_id = PrimaryKey(str)
    processed_file_path = Required(str, unique=True)
    raw_file_path = Required(str, unique=True)
    is_active = Required(bool)
    uploaded_at = Required(datetime, default=datetime.utcnow)


db.generate_mapping(create_tables=True)


class PostgreSQLInternalDatasetRepository(InternalDatasetRepository):
    def to_internal_dataset(
        self,
        internal_dataset_record: InternalDatasetModel
    ) -> InternalDataset:
        return InternalDataset(
            id=internal_dataset_record.id,
            processed_file_path=internal_dataset_record.processed_file_path,
            raw_file_path=internal_dataset_record.raw_file_path,
            is_active=internal_dataset_record.is_active,
            uploaded_at=internal_dataset_record.uploaded_at,
        )

    @db_session
    def save(self, internal_dataset: InternalDataset):
        InternalDatasetModel(
            internal_dataset_id=internal_dataset.id,
            processed_file_path=internal_dataset.processed_file_path,
            raw_file_path=internal_dataset.raw_file_path,
            is_active=internal_dataset.is_active,
            uploaded_at=internal_dataset.uploaded_at,
        )

    @db_session
    def get_by_id(self, internal_dataset_id: UUID) -> InternalDataset | None:
        internal_dataset_record = InternalDatasetModel[internal_dataset_id]
        if internal_dataset_record:
            return self.to_internal_dataset(internal_dataset_record)
    """
    TODO CHECK THIS FUNCTION TYPING 
    @db_session
    def get_all_files(self) -> List[InternalDataset] | []:
        query = select(internal_dataset for internal_dataset in InternalDatasetModel)
        all_internal_datasets = []
        for internal_dataset_record in query:
            internal_dataset = self.to_internal_dataset(
                    internal_dataset_record)
            all_internal_datasets.append(internal_dataset)
        return all_internal_datasets
    """

    @db_session
    def get_active_file(self) -> InternalDataset | None:
        internal_dataset_record = InternalDatasetModel.get(is_active=True)
        if internal_dataset_record:
            return self.to_internal_dataset(internal_dataset_record)

    @db_session
    def get_by_raw_file_path(
            self,
            raw_file_path: str
    ) -> InternalDataset | None:
        internal_dataset_record = InternalDatasetModel.get(
                raw_file_path=raw_file_path)
        if internal_dataset_record:
            return self.to_internal_dataset(internal_dataset_record)

    @db_session
    def get_by_processed_file_path(
        self,
        processed_file_path: str
    ) -> InternalDataset | None:
        internal_dataset_record = InternalDatasetModel.get(processed_file_path=processed_file_path)
        if internal_dataset_record:
            return self.to_internal_dataset(internal_dataset_record)
