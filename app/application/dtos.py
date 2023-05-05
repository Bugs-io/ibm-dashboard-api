from pydantic import BaseModel


class DatasetDTO(BaseModel):
    id: str
    processed_file_path: str
    raw_file_path: str


class UserDTO(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


class SignUpRequestDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class AuthRequestDTO(BaseModel):
    email: str
    password: str


class AuthResponseDTO(BaseModel):
    id: str
    email: str
    id_token: str
