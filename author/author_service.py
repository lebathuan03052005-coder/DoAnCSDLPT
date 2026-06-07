from flask import Flask, jsonify
from author_database import AuthorSessionLocal
from author_models import Author

app = Flask(__name__)

@app.route('/authors', methods=['GET'])
def get_authors():
    session = AuthorSessionLocal()
    try:
        # Query authors
        authors = session.query(Author).all()
        return jsonify([{"AuthorID": a.AuthorID, "Name": a.Name} for a in authors])
    finally:
        session.close()

if __name__ == '__main__':
    app.run(port=5001)