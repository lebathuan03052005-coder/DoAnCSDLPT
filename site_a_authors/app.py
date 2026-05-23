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
#  Khai báo hằng số độ trễ mạng 50ms ( điều chỉnh để thử nghiệm với các mức độ trễ khác nhau) 


# CHIẾN LƯỢC 1: LAZY LOADING

@app.route('/test/lazy', methods=['GET'])
def lazy_loading():
    limit = int(request.args.get('limit', 10))
    #  Dùng deepcopy để không làm hỏng dữ liệu gốc trong RAM
    authors_to_fetch = copy.deepcopy(authors_data[:limit]) 
    
    start_time = time.time()
    network_calls = 0
    
    for author in authors_to_fetch:
        time.sleep(NETWORK_LATENCY) #  Giả lập độ trễ cho MỖI request
        
        response = requests.get(f"{SITE_B_URL}/api/books/author/{author['AuthorID']}")
        
        # Chỉ gán sách khi request thành công (tránh lỗi nếu Site B sập)
        if response.status_code == 200:
            author['books'] = response.json()
        else:
            author['books'] = []
            
        network_calls += 1
        
    end_time = time.time()
    
    return jsonify({
        "strategy": "Lazy Loading (N+1)",
        "authors_count": limit,
        "network_calls": network_calls,
        "execution_time_ms": round((end_time - start_time) * 1000, 2)
    })


# CHIẾN LƯỢC 2: EAGER LOADING

@app.route('/test/eager', methods=['GET'])
def eager_loading():
    limit = int(request.args.get('limit', 10))
    # Dùng deepcopy để không làm hỏng dữ liệu gốc trong RAM
    authors_to_fetch = copy.deepcopy(authors_data[:limit]) 
    
    start_time = time.time()
    network_calls = 0
    
    time.sleep(NETWORK_LATENCY) # Giả lập độ trễ cho request duy nhất
    
    response = requests.get(f"{SITE_B_URL}/api/books/all")
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
            
    end_time = time.time()
    
    return jsonify({
        "strategy": "Eager Loading (1 Request Batch)",
        "authors_count": limit,
        "network_calls": network_calls,
        "execution_time_ms": round((end_time - start_time) * 1000, 2)
    })

if __name__ == '__main__':
    print("Author Service (Site A) đang chạy tại http://localhost:5001")
    app.run(port=5001, debug=True)