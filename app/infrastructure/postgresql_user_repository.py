from pony.orm import db_session, Database, PrimaryKey, Required
from app.application.ports import UserRepository
from app.domain.user import User

db = Database()
db.bind(
        provider='postgres',
        user='postgres',
        password='',
        host='localhost',
        database='ibm_dashboard'
        )


class UserModel(db.Entity):
    _table_ = "users"
    user_id = PrimaryKey(str)
    email = Required(str, unique=True)
    password = Required(str)


db.generate_mapping(create_tables=True)


class PostgreSQLUserRepository(UserRepository):
    @db_session
    def save(self, user: User):
        UserModel(user_id=user.id, email=user.email, password=user.password)

    @db_session
    def get_by_id(self, user_id: str) -> User:
        user = UserModel[user_id]
        return user

    @db_session
    def get_by_email(self, email: str) -> User:
        user = UserModel.get(email=email)
        return user
