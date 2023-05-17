from datetime import datetime
from pony.orm import Database, PrimaryKey, Required

from app.config import Config

DB = Database()


class UserModel(DB.Entity):
    _table_ = "users"
    user_id = PrimaryKey(str)
    first_name = Required(str)
    last_name = Required(str)
    email = Required(str, unique=True)
    password = Required(str)


class InternalDatasetModel(DB.Entity):
    _table_ = "internal_datasets"
    internal_dataset_id = PrimaryKey(str)
    processed_file_path = Required(str, unique=True)
    raw_file_path = Required(str, unique=True)
    is_active = Required(bool)
    uploaded_at = Required(datetime, default=datetime.utcnow)


def connect_to_db():
    DB.bind(
        provider=Config.DB_PROVIDER,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        )


def init_db():
    connect_to_db()
    DB.generate_mapping(create_tables=True)
