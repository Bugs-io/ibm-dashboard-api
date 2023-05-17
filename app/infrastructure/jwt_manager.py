from typing import Dict
from datetime import datetime, timedelta, timezone
import jwt

from app.application.ports import TokenManager


class JWTManager(TokenManager):
    def __init__(self, algorithm: str, secret_key: str, expiration_delta: str):
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.expiration_delta = expiration_delta

    def generate_token(self, payload: Dict[str, any]) -> str:
        expiration_date = datetime.now(timezone.utc)
        expiration_date += timedelta(milliseconds=self.expiration_delta)

        payload['exp'] = expiration_date.timestamp()

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token: str) -> Dict[str, any]:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
