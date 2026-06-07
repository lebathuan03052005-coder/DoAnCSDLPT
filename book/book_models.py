from sqlalchemy import Column, String, ForeignKey
from book_database import Base

class Book(Base):
    __tablename__ = 'books'
    BookID = Column(String(50), primary_key=True)
    AuthorID = Column(String(50)) # Chỉ lưu AuthorID như một field bình thường
    Title = Column(String(200))