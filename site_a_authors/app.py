from flask import Flask, jsonify, request
import json
import os
import time
import requests

app = Flask(__name__)

# Đọc dữ liệu Authors từ file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/authors.json')

with open(data_path, 'r', encoding='utf-8') as f:
    authors_data = json.load(f)

# Địa chỉ của Site B đang chạy
SITE_B_URL = "http://localhost:5002"

# CHIẾN LƯỢC 1: LAZY LOADING (Vấn đề N+1)
# Lấy danh sách Author, sau đó mỗi Author lại gọi 1 Request sang Site B
@app.route('/test/lazy', methods=['GET'])
def lazy_loading():
    # Lấy tham số 'limit' từ URL (mặc định thử nghiệm 10 tác giả)
    limit = int(request.args.get('limit', 10))
    authors_to_fetch = authors_data[:limit]
    
    start_time = time.time() # Bắt đầu bấm giờ
    network_calls = 0
    
    for author in authors_to_fetch:
        # GỌI N LẦN: Call API sang Site B cho từng tác giả
        response = requests.get(f"{SITE_B_URL}/api/books/author/{author['AuthorID']}")
        author['books'] = response.json()
        network_calls += 1
        
    end_time = time.time() # Kết thúc bấm giờ
    
    return jsonify({
        "strategy": "Lazy Loading (N+1)",
        "authors_count": limit,
        "network_calls": network_calls,
        "execution_time_ms": round((end_time - start_time) * 1000, 2)
    })

# -------------------------------------------------------------------
# CHIẾN LƯỢC 2: EAGER LOADING
# Gọi đúng 1 Request lấy toàn bộ sách về, sau đó tự map bằng code
# -------------------------------------------------------------------
@app.route('/test/eager', methods=['GET'])
def eager_loading():
    limit = int(request.args.get('limit', 10))
    authors_to_fetch = authors_data[:limit]
    
    start_time = time.time()
    network_calls = 0
    
    # GỌI 1 LẦN DUY NHẤT lấy toàn bộ dữ liệu Sách
    response = requests.get(f"{SITE_B_URL}/api/books/all")
    all_books = response.json()
    network_calls += 1
    
    # Kỹ thuật Map in-memory: Gom nhóm sách theo AuthorID cực nhanh
    books_by_author = {}
    for book in all_books:
        a_id = book['AuthorID']
        if a_id not in books_by_author:
            books_by_author[a_id] = []
        books_by_author[a_id].append(book)
        
    # Gán sách vào danh sách tác giả trả về
    for author in authors_to_fetch:
        author['books'] = books_by_author.get(author['AuthorID'], [])
        
    end_time = time.time()
    
    return jsonify({
        "strategy": "Eager Loading (1 Request Batch)",
        "authors_count": limit,
        "network_calls": network_calls,
        "execution_time_ms": round((end_time - start_time) * 1000, 2)
    })

if __name__ == '__main__':
    print(" Author Service (Site A) đang chạy tại http://localhost:5001")
    app.run(port=5001, debug=True)  