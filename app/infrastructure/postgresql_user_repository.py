from pony.orm import db_session, Database, PrimaryKey, Required
from app.application.ports import UserRepository
from app.domain import User

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
    def get_by_id(self, user_id: str) -> User | None:
        user_record = UserModel[user_id]

        if user_record:
            return User(
                    id=user_record.user_id,
                    email=user_record.email,
                    password=user_record.password
                    )

    @db_session
    def get_by_email(self, email: str) -> User | None:
        user_record = UserModel.get(email=email)

        if user_record:
            return User(
                    id=user_record.user_id,
                    email=user_record.email,
                    password=user_record.password
                    )
