from pydantic import BaseModel


class DatasetDTO(BaseModel):
    name: str
    path: str


class UserDTO(BaseModel):
    id: str
    email: str
