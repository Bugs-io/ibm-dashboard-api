from pony.orm import Database

from app.config import Config


class DatabaseSingleton():
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialize()
        return cls.__instance

    def __initialize(self):
        self.db = Database()
        if not Config.TESTING:
            self.connect_to_db()

    def generate_mapping(self):
        self.db.generate_mapping(create_tables=True)

    def connect_to_db(self):
        self.db.bind(
            provider=Config.DB_PROVIDER,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            database=Config.DB_NAME,
        )
        self.generate_mapping()
