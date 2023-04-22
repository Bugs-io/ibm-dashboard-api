from typing import Dict


class TokenManager:
    def generate_token(
            self,
            payload: Dict[str, any],
            milliseconds_to_expire: int
            ) -> str:
        pass

    def validate_token(self, token: str) -> Dict[str, any]:
        pass
