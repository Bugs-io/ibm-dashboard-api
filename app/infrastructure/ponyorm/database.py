from .DatabaseSingleton import DatabaseSingleton

db_singleton = DatabaseSingleton()
db = db_singleton.db
