# Đồ Án Cơ Sở Dữ Liệu Phân Tán: Phân Tích Hiệu Năng ORM

**Sinh viên thực hiện:** Lê Bá Thuần
**Giảng viên hướng dẫn:** Lê Hà Thanh
**Môn học:** Cơ sở dữ liệu phân tán
**Năm thực hiện:** 2026

---

## Tổng quan dự án

Đề tài tập trung nghiên cứu ảnh hưởng của **độ trễ mạng (Network Latency)** trong các hệ thống cơ sở dữ liệu phân tán khi sử dụng ORM (Object Relational Mapping).

Đồ án tiến hành so sánh hiệu năng giữa hai chiến lược truy xuất dữ liệu:

- **Lazy Loading (N+1 Problem):**
  - Mỗi đối tượng liên quan được truy vấn riêng biệt.
  - Làm gia tăng số lượng truy vấn qua mạng.
  - Dẫn đến suy giảm hiệu năng trong môi trường phân tán.

- **Eager Loading (Select IN / Batch Loading):**
  - Gom nhóm dữ liệu và truy xuất theo lô.
  - Giảm số lần giao tiếp giữa các Site.
  - Tối ưu thời gian phản hồi và băng thông mạng.

---

## Cấu trúc dự án

```text
DEMODOAN/
├── TaoDL_LuuVaoSQL/
│   ├── authors.json             # Dữ liệu tác giả
│   ├── books.json               # Dữ liệu sách
│   ├── generate_data.py         # Sinh dữ liệu tự động
│   └── import_data.py           # Nạp dữ liệu vào SQL Server
│
├── app.py                       # API Service (Site A)
├── database.py                  # Cấu hình kết nối SQL Server và ORM
├── models.py                    # Định nghĩa các Model (Author, Book)
├── test_runner.py               # Chạy kịch bản đo lường và vẽ biểu đồ
└── README.md                    # Tài liệu hướng dẫn
```

---

## Quy trình triển khai

### Bước 1: Sinh dữ liệu

Tạo dữ liệu tác giả và sách dưới dạng JSON:

```bash
python TaoDL_LuuVaoSQL/generate_data.py
```

---

### Bước 2: Nạp dữ liệu vào SQL Server

Import dữ liệu từ file JSON vào cơ sở dữ liệu bằng phương pháp Bulk Insert:

```bash
python TaoDL_LuuVaoSQL/import_data.py
```

---

### Bước 3: Chạy hệ thống và thực hiện Demo

Khởi động API Server:

```bash
python app.py
```

Chạy kịch bản đo lường:

```bash
python test_runner.py
```

Sau khi hoàn tất, hệ thống sẽ tự động sinh biểu đồ:

```text
n_plus_1_problem_chart.png
```

Biểu đồ dùng để so sánh hiệu năng giữa:

- Lazy Loading (N+1 Problem)
- Eager Loading (Batch Loading)

---

## Các cơ chế xử lý lỗi

### Fault Tolerance

Hệ thống được tích hợp cơ chế xử lý ngoại lệ `OperationalError`.

Trong trường hợp Database (Site B) bị ngắt kết nối trong quá trình thực hiện:

- API không bị dừng đột ngột.
- Hệ thống trả về mã lỗi **503 Service Unavailable**.
- Cung cấp thông báo trạng thái phù hợp cho người dùng.

---

### Auto-Recovery

Cơ chế bắt ngoại lệ và kết nối lại giúp:

- Duy trì tính ổn định của hệ thống phân tán.
- Hạn chế gián đoạn dịch vụ.
- Đảm bảo khả năng hoạt động liên tục của ứng dụng.

---

## Kết quả kiểm chứng

Thông qua việc giả lập độ trễ mạng **50 ms**, đồ án đã cung cấp bằng chứng thực nghiệm cho thấy:

### Lazy Loading (N+1 Problem)

- Phát sinh số lượng lớn truy vấn giữa các Site.
- Thời gian thực thi tăng mạnh khi độ trễ mạng xuất hiện.
- Hiệu năng suy giảm đáng kể trong môi trường phân tán.

### Eager Loading (Batch Loading)

- Giảm số lần giao tiếp giữa các Site.
- Tiết kiệm băng thông mạng.
- Rút ngắn thời gian xử lý.
- Đạt hiệu năng vượt trội so với Lazy Loading.

---

## Công nghệ sử dụng

- Python
- Flask
- SQLAlchemy ORM
- SQL Server
- PyODBC
- Matplotlib

---

## Kết luận

Đồ án đã chứng minh rằng trong môi trường cơ sở dữ liệu phân tán có độ trễ mạng, việc sử dụng **Eager Loading (Batch Loading)** giúp giảm đáng kể số lượng truy vấn qua mạng và cải thiện hiệu năng so với **Lazy Loading (N+1 Problem)**, từ đó nâng cao hiệu quả hoạt động của các hệ thống phân tán sử dụng ORM.
