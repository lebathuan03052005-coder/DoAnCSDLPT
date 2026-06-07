from sqlalchemy import Column, String
from author_database import Base

class Author(Base):
    __tablename__ = 'authors'
    AuthorID = Column(String(50), primary_key=True)
    Name = Column(String(100))
    Region = Column(String(200))
