from flask import Flask, jsonify
import json
import os
import time 

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/books.json')

with open(data_path, 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# API LAZY LOADING 
@app.route('/api/books/author/<int:author_id>', methods=['GET'])
def get_books_by_author(author_id):
    time.sleep(0.05) # Giả lập mạng chậm 50ms cho mỗi lượt lấy sách
    result = [book for book in books_data if book['AuthorID'] == author_id]
    return jsonify(result)

# API EAGER LOADING
@app.route('/api/books/all', methods=['GET'])
def get_all_books():
    time.sleep(0.05) # Mạng chậm 50ms, nhưng Eager chỉ phải chịu 1 lần duy nhất
    return jsonify(books_data)

if __name__ == '__main__':
    print("Book Service (Site B) đang chạy tại http://localhost:5002")
    app.run(port=5002, debug=True)