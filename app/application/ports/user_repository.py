from app.domain.user import User


class UserRepository:
    def save(self, user: User):
        pass

    def get_by_id(self, user_id: int) -> User | None:
        pass

    def get_by_email(self, email: str) -> User | None:
        pass
