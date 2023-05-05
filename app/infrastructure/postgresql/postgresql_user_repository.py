from pony.orm import db_session
from app.application.ports import UserRepository
from app.domain import User
from .postgresql_db import UserModel


class PostgreSQLUserRepository(UserRepository):
    def _to_user(
            self,
            user_record: UserModel
            ) -> User:
        return User(
                id=user_record.user_id,
                first_name=user_record.first_name,
                last_name=user_record.last_name,
                email=user_record.email,
                password=user_record.password
                )

    @db_session
    def save(self, user: User):
        UserModel(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user.password)

    @db_session
    def get_by_id(self, user_id: str) -> User | None:
        user_record = UserModel[user_id]

        if user_record:
            return self._to_user(user_record)

    @db_session
    def get_by_email(self, email: str) -> User | None:
        user_record = UserModel.get(email=email)

        if user_record:
            return self._to_user(user_record)
