from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

class Author(Base):
    __tablename__ = 'authors'
    AuthorID = Column(String(50), primary_key=True)
    Name = Column(String(100))
    Region = Column(String(200))
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'
    BookID = Column(String(50), primary_key=True)
    AuthorID = Column(String(50), ForeignKey('authors.AuthorID'))
    Title = Column(String(200))
    author = relationship("Author", back_populates="books")