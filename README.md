
# Demo: N+1 Query Problem - Lazy Loading vs Eager Loading

## Đề tài được thực hiện bởi: Lê Bá Thuần.
## Với sự hướng dẫn của giảng viên: Lê Hà Thanh.

## Mô tả dự án

Dự án demo so sánh hiệu suất giữa hai chiến lược truy xuất dữ liệu trong hệ thống Cơ sở dữ liệu phân tán:

- **Lazy Loading (N+1 Problem)**: Lấy danh sách tác giả, rồi với mỗi tác giả lại gọi 1 request qua mạng để lấy sách → Phát sinh quá nhiều network calls, chịu ảnh hưởng nặng nề bởi độ trễ mạng.
- **Eager Loading (Batch/In-memory)**: Lấy toàn bộ sách cùng lúc bằng 1 request duy nhất, sau đó ánh xạ (map) dữ liệu bằng code → Tối thiểu hóa network calls, tốc độ vượt trội.

*Điểm nổi bật:* Dự án sử dụng **2 Flask microservices** giao tiếp với nhau và có **tích hợp giả lập độ trễ mạng (50ms)** để phản ánh chân thực của môi trường phân tán thực tế.

---

## Cách thức Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
pip install requests matplotlib

```

### 2. Sinh dữ liệu (lần đầu)

```bash
python generate_data.py

```

Kết quả sẽ sinh ra:

* `data/authors.json` - 500 tác giả
* `data/books.json` - 25,000 cuốn sách

---

## Chạy dự án

Để dự án hoạt động, bạn cần **mở 3 Terminal (Command Prompt) riêng biệt**:

### Terminal 1: Chạy Site B (Books Service)

```bash
cd site_b_books
python app.py

```
> Kì vọng: `Book Service (Site B) đang chạy tại http://localhost:5002`

### Terminal 2: Chạy Site A (Authors Service)

```bash
cd site_a_authors
python app.py

```

> Kì vọng: `Author Service (Site A) đang chạy tại http://localhost:5001`

### Terminal 3: Chạy Kịch bản Test Tự động & Vẽ biểu đồ 

Đứng ở thư mục gốc của dự án, chạy lệnh:

```bash
python test_runner.py

```

**Kết quả:**
Script sẽ tự động đo lường thời gian chạy của cả 2 chiến lược với số lượng tác giả tăng dần (10, 30, 50, 100) và sinh ra file ảnh biểu đồ **`n_plus_1_problem_chart.png`** trực quan ngay tại thư mục gốc.

---

## Test API thủ công (Bằng cURL)

Nếu muốn tự kiểm tra từng API riêng lẻ để xem cấu trúc JSON trả về:

### Kiểm tra Lazy Loading (N+1 Problem)

```bash
curl "http://localhost:5001/test/lazy?limit=10"

```

**Lưu ý**: Với giả lập mạng 50ms, 10 tác giả (11 request) sẽ mất hơn nửa giây chỉ để chờ mạng.

### Kiểm tra Eager Loading (Batch Loading)

```bash
curl "http://localhost:5001/test/eager?limit=10"

```

**Kết quả**: Nhanh hơn gấp nhiều lần vì luôn chỉ mất 1 lần độ trễ mạng duy nhất!

---

## Cấu trúc file

```text
demoDoAn/
├── README.md
├── requirements.txt       # Dependencies
├── generate_data.py       # Sinh dữ liệu test
├── test_runner.py         # Kịch bản tự động test và vẽ biểu đồ báo cáo
├── n_plus_1_problem_chart.png # (Tự động sinh ra) Biểu đồ kết quả test
│
├── site_a_authors/        # Microservice Authors (Site A)
│   └── app.py             # Chứa /test/lazy & /test/eager
│
├── site_b_books/          # Microservice Books (Site B)
│   └── app.py             # Chứa /api/books/* endpoints
│
└── data/                  # Dữ liệu (sinh từ generate_data.py)
    ├── authors.json       # 500 tác giả
    └── books.json         # 25,000 cuốn sách

```

## Tuỳ chỉnh

### Thay đổi số lượng dữ liệu

Mở `generate_data.py` và sửa:

```python
NUM_AUTHORS = 500      # Tăng giảm số tác giả
NUM_BOOKS = 25000      # Tăng giảm số sách

```

Rồi chạy lại: `python generate_data.py`

## Tài liệu tham khảo

* [N+1 Query Problem](https://www.google.com/search?q=https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem)
* [Flask Documentation](https://flask.palletsprojects.com/)
* [Eager vs Lazy Loading](https://en.wikipedia.org/wiki/Lazy_loading)
