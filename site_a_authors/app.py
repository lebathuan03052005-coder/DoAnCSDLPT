from flask import Flask, jsonify, request # Thư viện Flask để xây dựng API
import json # Thư viện json để đọc dữ liệu từ file JSON
import os # Thư viện os để xử lý đường dẫn file
import time # Thư viện time để đo thời gian
import requests # Thư viện requests để gọi API giữa các service
import copy # Thư viện copy để chống lỗi tham chiếu bộ nhớ

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/authors.json')

with open(data_path, 'r', encoding='utf-8') as f:
    authors_data = json.load(f)

SITE_B_URL = "http://localhost:5002"
NETWORK_LATENCY = 0.05 
#  Khai báo hằng số độ trễ mạng 50ms 


# CHIẾN LƯỢC 1: LAZY LOADING
@app.route('/test/lazy', methods=['GET'])
def lazy_loading():
    limit = int(request.args.get('limit', 10))
    authors_to_fetch = copy.deepcopy(authors_data[:limit]) 
    
    start_time = time.time()
    network_calls = 0
    
    for author in authors_to_fetch:
        time.sleep(NETWORK_LATENCY)
        
        # Bắt đầu khối xử lý lỗi
        try:
            # Thêm timeout=1 để nếu Site B sập, nó sẽ báo lỗi ngay sau 1 giây thay vì treo
            response = requests.get(f"{SITE_B_URL}/api/books/author/{author['AuthorID']}", timeout=1)
            
            if response.status_code == 200:
                author['books'] = response.json()
            else:
                author['books'] = []
        except requests.exceptions.RequestException:
            # Nếu bắt được lỗi mất kết nối, hệ thống không crash mà gán cảnh báo
            author['books'] = "LOI: Book Service Site B hien dang mat ket noi!"
            
        network_calls += 1
        
    end_time = time.time()
    
    return jsonify({
        "strategy": "Lazy Loading (N+1)",
        "authors_count": limit,
        "network_calls": network_calls,
        "execution_time_ms": round((end_time - start_time) * 1000, 2),
        "data": authors_to_fetch 
    })


# CHIẾN LƯỢC 2: EAGER LOADING
@app.route('/test/eager', methods=['GET'])
def eager_loading():
    limit = int(request.args.get('limit', 10))
    authors_to_fetch = copy.deepcopy(authors_data[:limit]) 
    
    start_time = time.time()
    network_calls = 0
    
    time.sleep(NETWORK_LATENCY) 
    
    try:
        # Eager Loading gọi 1 lần duy nhất để lấy tất cả sách
        response = requests.get(f"{SITE_B_URL}/api/books/all", timeout=5)
        network_calls += 1
        
        if response.status_code == 200:
            all_books = response.json()
            
            # Map in-memory
            books_by_author = {}
            for book in all_books:
                a_id = book['AuthorID']
                if a_id not in books_by_author:
                    books_by_author[a_id] = []
                books_by_author[a_id].append(book)
                
            # Gán sách
            for author in authors_to_fetch:
                author['books'] = books_by_author.get(author['AuthorID'], [])
                
    except requests.exceptions.RequestException:
        # Nếu Site B sập, toàn bộ tác giả đều bị thiếu thông tin sách
        network_calls += 1
        for author in authors_to_fetch:
            author['books'] = "LOI: Book Service Site B hien dang mat ket noi!"
            
    end_time = time.time()
    
    return jsonify({
        "strategy": "Eager Loading (1 Request Batch)",
        "authors_count": limit,
        "network_calls": network_calls,
        "execution_time_ms": round((end_time - start_time) * 1000, 2),
        "data": authors_to_fetch
    })

if __name__ == '__main__':
    print("Author Service (Site A) đang chạy tại http://localhost:5001")
    app.run(port=5001, debug=True)