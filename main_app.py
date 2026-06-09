import requests
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/test/lazy')
def test_lazy():
    start_time = time.time()
    limit = int(request.args.get('limit', 10))
    network_calls = 0
    
    # 1. Lấy danh sách tác giả (Service A)
    try:
        authors = requests.get("http://localhost:5001/authors").json()
        authors = authors[:limit]
        network_calls += 1
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Author Service (A) không khả dụng"}), 503
    
    results = []
    # 2. Lazy Loading: Vòng lặp N+1
    # SELECT * FROM books WHERE AuthorID = ?;
    for author in authors:
        try:
            res = requests.get(f"http://localhost:5002/books/{author['AuthorID']}")
            network_calls += 1
            books = res.json()
            results.append({"author": author, "books": books})
        except requests.exceptions.ConnectionError:
            # Nếu Book Service (B) bị ngắt, ghi chú lại để không làm sập Gateway
            results.append({"author": author, "books": "Book Service (B) ngung hoat dong"})
            
    execution_time_ms = (time.time() - start_time) * 1000
    return jsonify({
        "execution_time_ms": round(execution_time_ms, 2),
        "network_calls": network_calls,
        "data": results
    })

@app.route('/test/eager')
def test_eager():
    start_time = time.time()
    limit = int(request.args.get('limit', 10))
    network_calls = 0
    
    # 1. Lấy danh sách tác giả (Service A)
    try:
        authors = requests.get("http://localhost:5001/authors").json()
        authors = authors[:limit]
        network_calls += 1
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Author Service (A) khong hoat dong"}), 503
    
    # 2. Eager Loading: Gom tất cả ID vào 1 request duy nhất
    ids = ",".join([str(a['AuthorID']) for a in authors])
    try:
        books_res = requests.get(f"http://localhost:5002/books?ids={ids}")
        network_calls += 1
        books = books_res.json()
        
        # Gom nhóm kết quả (Client-side join)
        #SELECT * FROM books WHERE AuthorID IN ('A001', 'A002', 'A003', ...);
        results = [{"author": a, "books": [b for b in books if b['AuthorID'] == a['AuthorID']]} for a in authors]
        
    except requests.exceptions.ConnectionError:
        results = [
            {
            "author": a,
            "books": [],
            "status": "Book Service (B) ngung hoat dong"
         }
         for a in authors
        ]
        
    execution_time_ms = (time.time() - start_time) * 1000
    return jsonify({
        "execution_time_ms": round(execution_time_ms, 2),
        "network_calls": network_calls,
        "data": results
    })

if __name__ == '__main__':
    # Chạy Gateway trên cổng 5000
    app.run(port=5000)