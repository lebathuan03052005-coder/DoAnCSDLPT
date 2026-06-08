# Đồ Án Cơ Sở Dữ Liệu Phân Tán: Phân tích vấn đề N+1 trong hệ cơ sở dữ liệu phân tán dưới ảnh hưởng của độ trễ mạng.

---

**Giảng viên hướng dẫn:** Lê Hà Thanh

**Sinh viên thực hiện:** Lê Bá Thuần

**Mã sinh viên:** N23DCCN059

**Môn học:** Cơ sở dữ liệu phân tán

---

# 1. Giới thiệu

Dự án nghiên cứu ảnh hưởng của độ trễ mạng (**Network Latency**) trong kiến trúc Microservices và cơ sở dữ liệu phân tán khi sử dụng ORM.

Bài toán được khảo sát là **N+1 Query Problem**, thông qua việc so sánh hai chiến lược truy xuất dữ liệu:

- **Lazy Loading (Sequential Fetching)**
- **Eager Loading / Batch Loading (Select IN Strategy)**

Mục tiêu của dự án là đánh giá tác động của số lượng round-trip mạng tới hiệu năng của hệ thống phân tán và chứng minh lợi ích của việc giảm số lượng message exchanges.

---

# 2. Kiến trúc hệ thống

Hệ thống được xây dựng theo mô hình **Database-per-Service** nhằm đảm bảo tính độc lập giữa các dịch vụ.

```
                     API Gateway
                     (Port 5000)
                           |
         --------------------------------------
         |                                    |
         |                                    |
 Author Microservice                    Book Microservice
     (Port 5001)                           (Port 5002)
         |                                    |
      AuthorDB                              BookDB
```

Trong đó:

- **Author Service** quản lý dữ liệu tác giả.
- **Book Service** quản lý dữ liệu sách.
- **API Gateway** đóng vai trò Aggregator, tổng hợp dữ liệu từ nhiều dịch vụ.

---

# 3. Cấu trúc thư mục

```
DEMODOAN/
│
├── author/                  # Author Microservice (Port 5001)
│
├── book/                    # Book Microservice (Port 5002)
│
├── TaoDLvsNapDL/            # Scripts tạo và nạp dữ liệu
│
├── main_app.py             # API Gateway / Aggregator (Port 5000)
│
├── test_runner.py          # Benchmark và sinh biểu đồ
│
├── requirements.txt
│
└── README.md
```

---

# 4. Cài đặt

## Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

# 5. Khởi tạo dữ liệu

Dữ liệu được lưu tách biệt theo mô hình Database-per-Service:

- AuthorDB
- BookDB

Chạy các script tạo dữ liệu:

```bash
python -m TaoDLvsNapDL.seeder_author
python -m TaoDLvsNapDL.seeder_book
```

---

# 6. Khởi chạy hệ thống

Khởi động các Microservices ở ba cửa sổ Terminal riêng biệt.

### Author Service

```bash
python -m author.author_service
```

Service chạy tại:

```
http://localhost:5001
```

---

### Book Service

```bash
python -m book.book_service
```

Service chạy tại:

```
http://localhost:5002
```

---

### API Gateway

```bash
python main_app.py
```

Gateway chạy tại:

```
http://localhost:5000
```

---

# 7. Chiến lược truy xuất dữ liệu

## 7.1 Lazy Loading

Gateway lấy danh sách Authors trước, sau đó gửi từng request riêng biệt tới Book Service.

```
Author Service
      ↓
Book Service (Author 1)
      ↓
Book Service (Author 2)
      ↓
...
      ↓
Book Service (Author N)
```

Đặc điểm:

- Phát sinh N+1 requests.
- Số lượng round-trip lớn.
- Hiệu năng suy giảm mạnh khi xuất hiện Network Latency.

---

## 7.2 Eager Loading (Batch Loading)

Gateway gom nhóm các AuthorID và gửi một request duy nhất tới Book Service.

```
Author Service
      ↓
Book Service
(SELECT ... WHERE AuthorID IN (...))
```

Đặc điểm:

- Chỉ cần 2 requests.
- Giảm số lần trao đổi message.
- Tối ưu thời gian phản hồi.

---

# 8. Benchmark

Chạy chương trình benchmark:

```bash
python test_runner.py
```

Kết quả sẽ sinh biểu đồ:

```
n_plus_1_problem_chart.png
```

Biểu đồ so sánh:

- Lazy Loading
- Eager Loading

trong các điều kiện độ trễ mạng khác nhau.

---

# 9. Fault Tolerance

Hệ thống được thiết kế để hoạt động ổn định trong môi trường phân tán, nơi các Microservices có thể tạm thời mất kết nối hoặc ngừng hoạt động.

## Fault Isolation

API Gateway đóng vai trò trung gian giữa Client và các Microservices. Khi một dịch vụ con gặp sự cố, lỗi được cô lập tại dịch vụ đó và không làm sập toàn bộ hệ thống.

### Trường hợp Author Service (Node A) không khả dụng

Nếu Gateway không thể kết nối tới Author Service:

```text
ConnectionError
```

Gateway sẽ trả về:

```http
503 Service Unavailable
```

Ví dụ:

```json
{
  "message": "Author Service (A) khong hoat dong"
}
```

Do dữ liệu tác giả là điểm khởi đầu của quá trình tổng hợp dữ liệu, Gateway không thể tiếp tục xử lý yêu cầu.

---

### Trường hợp Book Service (Node B) không khả dụng

#### Lazy Loading

Trong chiến lược Lazy Loading, Gateway thực hiện nhiều request độc lập tới Book Service.

Nếu Book Service bị ngắt kết nối trong quá trình xử lý, Gateway vẫn tiếp tục hoạt động và chỉ đánh dấu phần dữ liệu bị lỗi thay vì làm toàn bộ request thất bại.

Ví dụ:

```json
{
  "author": {
    "AuthorID": 1,
    "Name": "John"
  },
  "books": "Book Service (B) ngung hoat dong"
}
```

Cơ chế này giúp:

- Cô lập lỗi giữa các dịch vụ (Fault Isolation).
- Gateway không bị crash.
- Một phần dữ liệu vẫn được trả về cho Client.

---

#### Eager Loading

Trong chiến lược Eager Loading, toàn bộ dữ liệu sách được lấy bằng một request duy nhất.

Nếu Book Service không khả dụng:

```text
ConnectionError
```

Gateway sẽ trả về:

```http
503 Service Unavailable
```

Ví dụ:

```json
{
  "message": "Book Service (B) ngung hoat dong"
}
```

---

## Client-Side Join

Do dữ liệu được lưu trên hai Database độc lập:

- AuthorDB
- BookDB

Gateway không thực hiện Distributed JOIN ở tầng cơ sở dữ liệu.

Thay vào đó, Gateway:

1. Lấy dữ liệu Authors từ Author Service.
2. Lấy dữ liệu Books từ Book Service.
3. Thực hiện việc kết hợp dữ liệu trong RAM (Client-Side Join).

```text
Author Service
       ↓
Book Service
       ↓
API Gateway
       ↓
Client
```

Cách tiếp cận này mang lại các lợi ích:

- Giảm sự phụ thuộc giữa các Database.
- Tăng khả năng mở rộng (Scalability).
- Dễ dàng thay đổi hoặc triển khai độc lập từng Microservice.
- Phù hợp với mô hình Database-per-Service trong kiến trúc Microservices.

---

## Failure Scenario

Một kịch bản lỗi được sử dụng trong quá trình kiểm thử là:

```text
Tắt Book Service (Port 5002)
```

Kết quả:

- API Gateway vẫn hoạt động bình thường.
- Không xảy ra hiện tượng crash toàn hệ thống.
- Lỗi được giới hạn trong phạm vi Book Service.
- Client nhận được thông báo lỗi hoặc dữ liệu không đầy đủ tùy theo chiến lược truy xuất dữ liệu.

Điều này minh họa đặc tính Fault Tolerance và Fault Isolation của hệ thống phân tán.

# 10. Kết quả thực nghiệm

Khi mô phỏng độ trễ mạng 50 ms:

### Lazy Loading

- Thời gian phản hồi tăng gần tuyến tính theo số lượng Authors.
- Phát sinh nhiều HTTP Requests.
- Communication Cost chiếm ưu thế.

### Eager Loading

- Thời gian phản hồi ổn định.
- Giảm đáng kể số lượng Round-trip.
- Hiệu năng vượt trội trong môi trường phân tán.

---

# 11. Kết luận

Đồ án chứng minh rằng trong hệ thống phân tán, việc tối ưu số lượng message exchanges quan trọng hơn việc chỉ tối ưu truy vấn SQL cục bộ.

Việc chuyển từ:

```
Lazy Loading
```

sang:

```
Eager Loading (Batch Query)
```

kết hợp với:

```
API Aggregation
```

giúp:

- Giảm Communication Cost.
- Giảm số lượng Round-trip.
- Cải thiện thời gian phản hồi.
- Tăng khả năng mở rộng của kiến trúc Microservices.

---

# Công nghệ sử dụng

- Python
- Flask
- SQLAlchemy ORM
- SQL Server
- REST API
- Matplotlib
- Requests

---

# Chủ đề liên quan

- Distributed Database Systems
- Distributed Query Processing
- Communication Cost
- Network Latency
- N+1 Query Problem
- Batch Query
- API Aggregation Pattern
- Database-per-Service Architecture
- Fault Tolerance
- Microservices Architecture
