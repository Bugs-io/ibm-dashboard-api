from pony.orm import Database

from app.config import Config

db = Database()


def connect_to_db():
    db.bind(
        provider=Config.DB_PROVIDER,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        )
    db.generate_mapping(create_tables=True)


def init_db():
    if not Config.TESTING:
        connect_to_db()
