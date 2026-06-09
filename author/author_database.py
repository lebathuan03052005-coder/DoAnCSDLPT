import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Kết nối thông qua thư viện sqlaichemy
AUTHOR_DATABASE_URL = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-03TS7J6;DATABASE=AuthorDB;Trusted_Connection=yes;"
author_engine = create_engine(AUTHOR_DATABASE_URL)
AuthorSessionLocal = sessionmaker(bind=author_engine)
Base = declarative_base()