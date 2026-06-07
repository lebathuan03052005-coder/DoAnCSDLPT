import json
import random
from faker import Faker
import os

fake = Faker()

# Cấu hình số lượng
NUM_AUTHORS = 500
NUM_BOOKS = 25000

def generate_data():
    print("Đang sinh dữ liệu Authors...")
    authors = []
    author_ids = []
    
    for i in range(1, NUM_AUTHORS + 1):
        author_id = f"A{i:04d}"
        author_ids.append(author_id)
        authors.append({
            "AuthorID": author_id,
            "Name": fake.name(),
            "Country": fake.country()
        })

    print("Đang sinh dữ liệu Books...")
    books = []
    for i in range(1, NUM_BOOKS + 1):
        books.append({
            "BookID": f"B{i:05d}",
            "AuthorID": random.choice(author_ids), # Random tác giả từ danh sách trên
            "Title": fake.sentence(nb_words=4).rstrip('.'),
            "CreatedAt": fake.date_time_this_decade().isoformat()
        })

    # Lưu ra file JSON
    print("Đang lưu ra file JSON...")
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)
        
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"Hoàn tất! Đã tạo {len(authors)} authors và {len(books)} books.")

if __name__ == "__main__":
    generate_data()