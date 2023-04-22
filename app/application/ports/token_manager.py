from typing import Dict


class TokenManager:
    def generate_token(self, payload: Dict[str, any]) -> str:
        pass

    def validate_token(self, token: str) -> Dict[str, any]:
        pass
