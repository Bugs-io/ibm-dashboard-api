from pydantic import BaseModel


class DatasetDTO(BaseModel):
    name: str
    path: str


class UserDTO(BaseModel):
    id: str
    email: str


class AuthRequestDTO(BaseModel):
    email: str
    password: str


class AuthResponseDTO(BaseModel):
    id: str
    email: str
    id_token: str
