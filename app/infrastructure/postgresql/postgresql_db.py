import os
from pony.orm import Database, PrimaryKey, Required
from dotenv import load_dotenv
from datetime import datetime

DB = Database()


class UserModel(DB.Entity):
    _table_ = "users"
    user_id = PrimaryKey(str)
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
        provider=os.getenv('DB_PROVIDER'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME')
        )


def init_db():
    load_dotenv()

    connect_to_db()

    DB.generate_mapping(create_tables=True)
