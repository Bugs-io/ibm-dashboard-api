from os import path, remove
from datetime import datetime
from io import BytesIO
from typing import List
from tempfile import NamedTemporaryFile
from uuid import uuid4
from kink import inject
import magic

from app.application.ports import ObjectStorage, UserRepository,\
        Encrypter, TokenManager, InternalDatasetRepository,\
        DataAnalysisGateway
from app.application.errors import InvalidFileTypeError, InvalidEmailError,\
    UserAlreadyExistsError, UserCreationError, UserDoesNotExistError,\
    InvalidPasswordError, InternalDatasetCreationError, InvalidNameError,\
    DatasetNotFound, DatasetNotAvailable
from app.application.dtos import DatasetDTO, AuthRequestDTO, AuthResponseDTO,\
        SignUpRequestDTO, UserDTO
from app.domain import InternalDataset, User, File

SPREADSHEET_MIME_TYPES = [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]

CSV_MIME_TYPE = ["text/csv"]

EMAIL_DOMAIN = "@ibm.com"


@inject
class IBMDashboardService:
    def __init__(
            self,
            encrypter: Encrypter,
            object_storage: ObjectStorage,
            token_manager: TokenManager,
            user_repository: UserRepository,
            internal_dataset_repository: InternalDatasetRepository,
            data_analysis_gateway: DataAnalysisGateway
            ):
        self.encrypter = encrypter
        self.object_storage = object_storage
        self.token_manager = token_manager
        self.user_repository = user_repository
        self.internal_dataset_repository = internal_dataset_repository
        self.data_analysis_gateway = data_analysis_gateway

    def get_all_internal_datasets(self):
        internal_datasets = self.internal_dataset_repository.get_all_files()
        return internal_datasets

    def _convert_file_to_bytes(self, file_content) -> bytes:
        byte_stream = BytesIO()
        byte_stream.write(file_content.encode('utf-8'))
        return byte_stream.getvalue()

    def _get_active_internal_dataset(self) -> File:
        active_internal_dataset = self.internal_dataset_repository.get_active_dataset()

        if not active_internal_dataset:
            raise DatasetNotAvailable

        tempfile = NamedTemporaryFile(delete=False)
        tempfile_path = tempfile.name

        blob_path = active_internal_dataset.processed_file_path

        try:
            self.object_storage.download_internal_dataset_from_url(
                    blob_path,
                    tempfile_path
                    )
        except Exception as exc:
            raise DatasetNotFound from exc

        with open(tempfile_path, 'r') as f:
            csv_content = f.read()

        byte_content = self._convert_file_to_bytes(csv_content)

        return File(tempfile_path, byte_content)

    def _upload_raw_internal_dataset(self, file_name: str, file_content: bytes) -> str:
        if not self._is_valid_file(file_content, SPREADSHEET_MIME_TYPES):
            raise InvalidFileTypeError

        return self.object_storage.upload_raw_internal_dataset(
                file_name,
                file_content
                )

    def _upload_processed_internal_dataset(self, file_name: str, file_content: bytes) -> str:
        return self.object_storage.upload_processed_internal_dataset(
                file_name,
                file_content
                )

    def upload_internal_dataset(self, file_name: str, file_content: bytes):
        file_id = self._get_uuid_as_str()
        file_name, file_extension = path.splitext(file_name)

        raw_file_name = f"{file_id}-{file_name}{file_extension}"
        processed_file_name = f"{file_id}-{file_name}.csv"

        processed_file_content = self.data_analysis_gateway.clean_internal_dataset(
                dataset=File(file_name, file_content)
                )
        processed_file_path = self._upload_processed_internal_dataset(
                file_name=processed_file_name,
                file_content=processed_file_content
                )

        raw_file_path = self._upload_raw_internal_dataset(
                file_name=raw_file_name,
                file_content=file_content
                )

        dataset_id = self._get_uuid_as_str()
        dataset = InternalDataset(
                id=dataset_id,
                processed_file_path=processed_file_path,
                raw_file_path=raw_file_path,
                is_active=True,
                uploaded_at=datetime.utcnow()
                )

        try:
            self.internal_dataset_repository.update_active_internal_dataset()
            self.internal_dataset_repository.save(dataset)
        except Exception as exc:
            raise InternalDatasetCreationError from exc
        return DatasetDTO(
                id=dataset.id,
                processed_file_path=dataset.processed_file_path,
                raw_file_path=dataset.raw_file_path)

    def signup(self, input_dto: SignUpRequestDTO) -> AuthResponseDTO:
        email = input_dto.email
        password = input_dto.password
        first_name = input_dto.first_name
        last_name = input_dto.last_name

        if EMAIL_DOMAIN not in email:
            raise InvalidEmailError

        if self.user_repository.get_by_email(email):
            raise UserAlreadyExistsError

        if len(first_name) == 0 or len(last_name) == 0:
            raise InvalidNameError

        hashed_password = self.encrypter.encrypt_password(password)

        user = User(
                id=str(uuid4()),
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password
                )

        try:
            self.user_repository.save(user)
        except Exception as exc:
            raise UserCreationError from exc

        token = self.token_manager.generate_token({"user_id": user.id})

        return AuthResponseDTO(id=user.id, email=user.email, id_token=token)

    def login(self, input_dto: AuthRequestDTO) -> AuthResponseDTO:
        email = input_dto.email
        password = input_dto.password

        user = self.user_repository.get_by_email(email)
        if not user:
            raise UserDoesNotExistError

        if not self.encrypter.check_password(password, user.password):
            raise InvalidPasswordError

        token = self.token_manager.generate_token({"user_id": user.id})

        return AuthResponseDTO(id=user.id, email=user.email, id_token=token)

    def get_user_by_id(self, user_id: str) -> UserDTO:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise UserDoesNotExistError

        return UserDTO(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
                )

    def get_most_attended_certifications(self, time_frame: str, limit: int):
        active_dataset = self._get_active_internal_dataset()
        since_years = time_frame_to_years(time_frame)

        result = self.data_analysis_gateway.get_most_attended_certifications(
                active_dataset,
                since_years,
                limit
                )

        remove(active_dataset.name)

        return result

    def _is_valid_file(
            self,
            file_content: bytes,
            file_types: List[str]
            ) -> bool:
        file_type = magic.from_buffer(file_content, mime=True)
        return file_type in file_types

    def _get_uuid_as_str(self) -> str:
        return str(uuid4())


def time_frame_to_years(time_frame: str) -> int | None:
    print(time_frame)
    years = {
            "last_year": 1,
            "last_5_years": 5,
            "last_10_years": 10,
            "all_time": 100
            }

    return years.get(time_frame)
