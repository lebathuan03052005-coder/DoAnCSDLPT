import sys
import os
import json

# Đường dẫn này sẽ trỏ từ 'TaoDL_LuuVaoSQL' ngược ra thư mục gốc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal, Base
from models import Author, Book
# Xóa sạch bảng cũ để làm mới hoàn toàn
Base.metadata.drop_all(bind=engine)
# Tạo lại bảng mới
Base.metadata.create_all(bind=engine)

def import_data_bulk():
    session = SessionLocal()
    print("Đang bắt đầu bơm dữ liệu siêu tốc...")
    
    try:
        # Bơm tác giả
        with open('authors.json', 'r', encoding='utf-8') as f:
            authors_data = json.load(f)
            # Chuyển đổi key nếu cần thiết
            authors_list = [{"AuthorID": item['AuthorID'], "Name": item['Name'], "Region": item.get('Country', 'Unknown')} for item in authors_data]
            session.bulk_insert_mappings(Author, authors_list)
        
        # Bơm sách
        with open('books.json', 'r', encoding='utf-8') as f:
            books_data = json.load(f)
            books_list = [{"BookID": item['BookID'], "AuthorID": item['AuthorID'], "Title": item['Title']} for item in books_data]
            session.bulk_insert_mappings(Book, books_list)
            
        session.commit()
        print(" Xong! Toàn bộ dữ liệu đã nằm gọn trong SQL Server.")
    except Exception as e:
        session.rollback()
        print(f" Lỗi rồi: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    import_data_bulk()