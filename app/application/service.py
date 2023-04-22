import magic
import uuid

from kink import inject
from app.application.ports import ObjectStorage, UserRepository,\
        Encrypter, TokenManager
from app.application.errors import InvalidFileTypeError, InvalidEmailError,\
    UserAlreadyExistsError, UserCreationError, UserDoesNotExistError,\
    InvalidPasswordError
from app.application.dtos import DatasetDTO, AuthRequestDTO, AuthResponseDTO
from app.domain import InternalDataset, User

SPREADSHEET_MIME_TYPES = [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]

EMAIL_DOMAIN = "@ibm.com"


@inject
class IBMDashboardService:
    def __init__(
            self,
            encrypter: Encrypter,
            object_storage: ObjectStorage,
            token_manager: TokenManager,
            user_repository: UserRepository
            ):
        self.encrypter = encrypter
        self.object_storage = object_storage
        self.token_manager = token_manager
        self.user_repository = user_repository

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
