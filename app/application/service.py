import magic
import uuid
from kink import inject
from app.application.ports import ObjectStorage, UserRepository,\
        Encrypter, TokenManager, InternalDatasetRepository
from app.application.errors import InvalidFileTypeError, InvalidEmailError,\
    UserAlreadyExistsError, UserCreationError, UserDoesNotExistError,\
    InvalidPasswordError
from app.application.dtos import DatasetDTO, AuthRequestDTO, AuthResponseDTO
from app.domain import InternalDataset, User
from typing import List
from uuid import uuid4
from datetime import datetime
import csv

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
            internal_dataset_repository: InternalDatasetRepository
            ):
        self.encrypter = encrypter
        self.object_storage = object_storage
        self.token_manager = token_manager
        self.user_repository = user_repository
        self.internal_dataset_repository = internal_dataset_repository

    def _is_valid_file(
            self,
            file_content: bytes,
            file_types: List[str]
            ) -> bool:
        file_type = magic.from_buffer(file_content, mime=True)
        return file_type in file_types

    def upload_raw_internal_dataset(
            self,
            file_name: str,
            file_content: bytes
            ) -> str:
        if not self._is_valid_file(file_content, SPREADSHEET_MIME_TYPES):
            raise InvalidFileTypeError

        raw_file_path = self.object_storage.upload_raw_internal_dataset(
                file_name,
                file_content
                )
        return raw_file_path

    def upload_processed_internal_dataset(
            self,
            file_name: str,
            file_content: bytes) -> str:
        #if not self._is_valid_file(file_content, CSV_MIME_TYPE):
        #   raise InvalidFileTypeError

        path = self.object_storage.upload_processed_internal_dataset(
                file_name,
                file_content
                )
        return path

    def upload_files(self, file_name: str, file_content: bytes):
        raw_file_path = self.upload_raw_internal_dataset(
                file_name=file_name,
                file_content=file_content)

        # TODO: call data analysis IBMDashboardService
        self.call_analysis_service()

        # Open the CSV file
        file_name = "file_example.csv"
        with open('file_example.csv', 'r') as csvfile:
            # Read the contents of the CSV file into a list of rows
            rows = list(csv.reader(csvfile))

        # Convert the rows to a byte string
        file_content = bytes('\n'.join([','.join(row) for row in rows]), encoding='utf-8')
        processed_file_path = self.upload_processed_internal_dataset(
                file_name=file_name,
                file_content=file_content
                )
        dataset = InternalDataset(
                id=str(uuid4()),
                processed_file_path=processed_file_path,
                raw_file_path=raw_file_path,
                is_active=True,
                uploaded_at=datetime.utcnow()
            )

        self.internal_dataset_repository.save(dataset)

        return DatasetDTO(
                id=dataset.id,
                processed_file_path=dataset.processed_file_path,
                raw_file_path=dataset.raw_file_path)

    def signup(self, input_dto: AuthRequestDTO) -> AuthResponseDTO:
        email = input_dto.email
        password = input_dto.password

        if EMAIL_DOMAIN not in email:
            raise InvalidEmailError

        if self.user_repository.get_by_email(email):
            raise UserAlreadyExistsError

        hashed_password = self.encrypter.encrypt_password(password)

        user = User(
                id=str(uuid.uuid4()),
                email=email,
                password=hashed_password
                )

        try:
            self.user_repository.save(user)
        except Exception:
            raise UserCreationError

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
