from sqlmodel import SQLModel, create_engine

class DatabaseEngine:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db")

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
