from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  

# Define the base class for the models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    github_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, github_id={self.github_id})>"

# Database connection URL
DATABASE_URL = "sqlite:///github_users.db"  # Use SQLite for simplicity

# Create an engine to interact with the database
engine = create_engine(DATABASE_URL, echo=True)

# Create the users table
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
