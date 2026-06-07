import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BOOK_DATABASE_URL = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-03TS7J6;DATABASE=BookDB;Trusted_Connection=yes;"
book_engine = create_engine(BOOK_DATABASE_URL)
BookSessionLocal = sessionmaker(bind=book_engine)
Base = declarative_base()