import json
import os
import sys
# Thêm thư mục gốc (demoDoAn) vào sys.path để Python tìm thấy folder 'author'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from author.author_database import AuthorSessionLocal, Base, author_engine
from author.author_models import Author

# Xóa bảng cũ nếu tồn tại và tạo lại bảng mới
Base.metadata.drop_all(bind=author_engine)
# Tạo bảng trong AuthorDB
Base.metadata.create_all(bind=author_engine)

def import_authors():
    session = AuthorSessionLocal()
    print("Đang nạp dữ liệu vào AuthorDB...")
    try:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'authors.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Chuẩn hóa dữ liệu theo model Author
            mappings = [{"AuthorID": i['AuthorID'], "Name": i['Name'], "Region": i.get('Country', 'Unknown')} for i in data]
            session.bulk_insert_mappings(Author, mappings)
        session.commit()
        print(" Xong! Authors đã được nạp.")
    except Exception as e:
        session.rollback()
        print(f" Lỗi nạp Authors: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    import_authors()