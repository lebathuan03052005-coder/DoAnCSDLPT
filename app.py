from flask import Flask, jsonify, request
import time
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import OperationalError  # <-- THÊM THƯ VIỆN BẮT LỖI MẠNG/DATABASE

# Import cấu hình và models từ 2 file vừa tạo
from database import engine, SessionLocal, Base, reset_network_calls, get_network_calls
from models import Author, Book

app = Flask(__name__)

# Tự động tạo bảng vào SQL Server nếu chưa có
Base.metadata.create_all(bind=engine)

@app.route('/test/lazy', methods=['GET'])
def lazy_loading():
    reset_network_calls() # Làm mới bộ đếm mạng
    limit = int(request.args.get('limit', 10))
    
    session = SessionLocal()
    start_time = time.time()
    
    try:
        # Bị lỗi N+1 tại đây do cơ chế mặc định
        authors = session.query(Author).limit(limit).all()
        
        result_data = []
        for author in authors:
            books_data = [{"BookID": b.BookID, "Title": b.Title} for b in author.books]
            result_data.append({
                "AuthorID": author.AuthorID,
                "Name": author.Name,
                "books": books_data
            })
            
        end_time = time.time()
        
        return jsonify({
            "strategy": "Lazy Loading (N+1)",
            "authors_count": len(authors),
            "network_calls": get_network_calls(),
            "execution_time_ms": round((end_time - start_time) * 1000, 2),
            "data": result_data
        })
        
    except OperationalError:
        # BẮT LỖI KHI SITE B (SQL SERVER) BỊ SẬP HOẶC MẤT MẠNG
        return jsonify({
            "status": "error",
            "message": "Canh bao: khong the ket noi den Data Node (Site B). He thong dang tam thoi gian doan.",
            "error_code": "NODE_B_OFFLINE"
        }), 503
        
    finally:
        # Đảm bảo luôn đóng kết nối an toàn dù thành công hay sập mạng
        session.close()

@app.route('/test/eager', methods=['GET'])
def eager_loading():
    reset_network_calls() # Làm mới bộ đếm mạng
    limit = int(request.args.get('limit', 10))
    
    session = SessionLocal()
    start_time = time.time()
    
    try:
        # Giải quyết bằng selectinload()
        authors = session.query(Author)\
                         .options(selectinload(Author.books))\
                         .limit(limit).all()
        
        result_data = []
        for author in authors:
            books_data = [{"BookID": b.BookID, "Title": b.Title} for b in author.books]
            result_data.append({
                "AuthorID": author.AuthorID,
                "Name": author.Name,
                "books": books_data
            })
            
        end_time = time.time()
        
        return jsonify({
            "strategy": "Eager Loading (Select IN)",
            "authors_count": len(authors),
            "network_calls": get_network_calls(),
            "execution_time_ms": round((end_time - start_time) * 1000, 2),
            "data": result_data
        })
        
    except OperationalError:
        # BẮT LỖI KHI SITE B (SQL SERVER) BỊ SẬP HOẶC MẤT MẠNG
        return jsonify({
            "status": "error",
            "message": "Canh bao: khong the ket noi den Data Node (Site B). He thong dang tam thoi gian doan.",
            "error_code": "NODE_B_OFFLINE"
        }), 503
        
    finally:
        session.close()

if __name__ == '__main__':
    print(" Server API đang chạy tại http://localhost:5001")
    app.run(port=5001, debug=True)