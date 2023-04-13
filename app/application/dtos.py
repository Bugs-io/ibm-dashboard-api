from pydantic import BaseModel


class DatasetDTO(BaseModel):
    name: str
    path: str
