import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Tạo bảng trong BookDB
from book.book_database import BookSessionLocal, Base, book_engine
from book.book_models import Book

Base.metadata.drop_all(bind=book_engine)
Base.metadata.create_all(bind=book_engine)

def import_books():
    session = BookSessionLocal()
    print("Đang nạp dữ liệu vào BookDB...")
    try:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Chuẩn hóa dữ liệu theo model Book
            mappings = [{"BookID": i['BookID'], "AuthorID": i['AuthorID'], "Title": i['Title']} for i in data]
            session.bulk_insert_mappings(Book, mappings)
        session.commit()
        print(" Xong! Books đã được nạp.")
    except Exception as e:
        session.rollback()
        print(f" Lỗi nạp Books: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    import_books()