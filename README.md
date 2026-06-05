# Đồ Án Cơ Sở Dữ Liệu Phân Tán: Phân Tích Hiệu Năng ORM

## Sinh viên thực hiện: Lê Bá Thuần

## Giảng viên hướng dẫn: Lê Hà Thanh

## Môn học: Cơ sở dữ liệu phân tán

## Tổng quan dự án:

### Đề tài:Dự án tập trung nghiên cứu sự ảnh hưởng của độ trễ mạng (Network Latency) trong các hệ thống phân tán khi sử dụng ORM. Đồ án so sánh hiệu năng giữa:

- Lazy Loading (N+1 Problem): Gây ra tình trạng quá tải số lượng truy vấn qua mạng.

- Eager Loading (Select IN): Tối ưu hóa truy vấn bằng cách gom nhóm dữ liệu (Batch Loading).

### Cấu trúc dự án

Plaintext
DEMODOAN/
├── TaoDL_LuuVaoSQL/ # Chứa dữ liệu và script xử lý
│ ├── authors.json # Dữ liệu tác giả
│ ├── books.json # Dữ liệu sách
│ ├── generate_data.py # Script sinh dữ liệu tự động
│ └── import_data.py # Script nạp dữ liệu vào SQL Server
├── app.py # API Service (Site A)
├── database.py # Cấu hình kết nối SQL Server & ORM
├── models.py # Định nghĩa các model (Author, Book)
├── test_runner.py # Script chạy kịch bản đo lường & vẽ biểu đồ
└── README.md # Tài liệu hướng dẫn

### Quy trình triển khai (3 bước)

- Bước 1: Sinh dữ liệu thô:
  Tạo file JSON chứa thông tin tác giả và sách:

Bash
python TaoDL_LuuVaoSQL/generate_data.py

- Bước 2: Nạp dữ liệu vào SQL Server
  Bơm dữ liệu từ file JSON vào Database (Bulk Insert để tối ưu thời gian):

Bash
python TaoDL_LuuVaoSQL/import_data.py
Bước 3: Chạy hệ thống & Demo
Chạy API Server:

Bash
python app.py
Chạy kịch bản đo lường:

Bash
python test_runner.py
Hệ thống sẽ tự động xuất file biểu đồ n_plus_1_problem_chart.png để so sánh hiệu năng.

⚙️ Các tính năng xử lý lỗi
Fault Tolerance: Hệ thống được tích hợp cơ chế bắt lỗi OperationalError. Nếu Database (Site B) bị ngắt kết nối trong lúc demo, API sẽ trả về mã lỗi 503 kèm thông báo trạng thái, đảm bảo ứng dụng không bị crash.

Auto-Recovery: Khả năng kết nối lại và xử lý ngoại lệ giúp hệ thống phân tán duy trì tính ổn định.

### Kết quả kiểm chứng

Bằng việc giả lập độ trễ mạng (50ms), đồ án cung cấp bằng chứng thực nghiệm về:

Sự suy giảm hiệu năng nghiêm trọng của Lazy Loading trong môi trường phân tán.

Sự ưu việt của Eager Loading trong việc tối ưu hóa băng thông và thời gian thực thi.

Đồ án môn Cơ sở dữ liệu phân tán - 2026
