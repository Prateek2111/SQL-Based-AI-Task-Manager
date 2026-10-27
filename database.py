from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


Database_URL = "sqlite:///todos.db"  # Using SQLite for simplicity; replace with your database URL

engine = create_engine(Database_URL);
LocalSession = sessionmaker(bind=engine);

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="pending")  # e.g., pending, completed
    priority = Column(String(20), default="medium")  # e.g., low, medium, high
    due_date = Column(String(50), default="")  # Store due date as string for simplicity
    created_at = Column(String(50), nullable=False)  # Store created date as string for simplicity 

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at,
        }

def init_db():
    Base.metadata.create_all(engine)  # Create tables based on the defined models