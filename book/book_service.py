from flask import Flask, request, jsonify
from book_database import BookSessionLocal 
from book_models import Book               

app = Flask(__name__)

# Lazy: GET /books/<author_id>
@app.route('/books/<author_id>', methods=['GET'])
def get_books_lazy(author_id):
    session = BookSessionLocal()
    try:
        # Truy vấn sách theo AuthorID
        books = session.query(Book).filter(Book.AuthorID == author_id).all()
        # Chuyển đổi dữ liệu sang list dict để trả về JSON
        return jsonify([{"BookID": b.BookID, "Title": b.Title} for b in books])
    finally:
        session.close()

# Eager: GET /books?ids=1,2,3
@app.route('/books', methods=['GET'])
def get_books_eager():
    ids_string = request.args.get('ids')
    if not ids_string:
        return jsonify([])
    
    ids = ids_string.split(',')
    session = BookSessionLocal()
    try:
        # Truy vấn sử dụng mệnh đề IN của SQL
        books = session.query(Book).filter(Book.AuthorID.in_(ids)).all()
        return jsonify([{"BookID": b.BookID, "Title": b.Title, "AuthorID": b.AuthorID} for b in books])
    finally:
        session.close()

if __name__ == '__main__':
    app.run(port=5002)