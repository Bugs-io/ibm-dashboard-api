from passlib.context import CryptContext
from app.application.ports import Encrypter


class BcryptEncrypter(Encrypter):
    def __init__(self):
        self.encryption_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto"
                )

    def encrypt_password(self, password: str) -> str:
        return self.encryption_context.hash(password)

    def check_password(self, password: str, hashed_password: str) -> bool:
        return self.encryption_context.verify(password, hashed_password)
