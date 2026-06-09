from flask import Flask, jsonify, request
from author_database import AuthorSessionLocal
from author_models import Author

app = Flask(__name__)

@app.route('/authors')
def get_authors():

    limit = int(request.args.get('limit', 10))

    session = AuthorSessionLocal()

    try:
        authors = session.query(Author).limit(limit).all()

        return jsonify([
            {
                "AuthorID": a.AuthorID,
                "Name": a.Name
            }
            for a in authors
        ])

    finally:
        session.close()

if __name__ == '__main__':
    app.run(port=5001)