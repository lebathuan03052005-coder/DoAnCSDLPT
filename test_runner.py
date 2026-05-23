import requests
import matplotlib.pyplot as plt

# Địa chỉ của Site A (Author Service)
SITE_A_URL = "http://localhost:5001"

# Các mốc số lượng Tác giả cần test
author_limits = [10, 30, 50, 100]

lazy_times = []
eager_times = []

print("Bắt đầu chạy kịch bản Test...\n" + "-"*40)

for limit in author_limits:
    print(f" Đang test với {limit} tác giả...")
    
    # 1. Test Lazy Loading
    res_lazy = requests.get(f"{SITE_A_URL}/test/lazy?limit={limit}").json()
    lazy_time = res_lazy['execution_time_ms']
    lazy_times.append(lazy_time)
    print(f"   - Lazy Loading: {lazy_time} ms (Số lần gọi mạng: {res_lazy['network_calls']})")
    
    # 2. Test Eager Loading
    res_eager = requests.get(f"{SITE_A_URL}/test/eager?limit={limit}").json()
    eager_time = res_eager['execution_time_ms']
    eager_times.append(eager_time)
    print(f"   - Eager Loading: {eager_time} ms (Số lần gọi mạng: {res_eager['network_calls']})")
    print("-" * 40)

print("\nĐã test xong! Đang vẽ biểu đồ...")

# ---------------------------------------------------------
# PHẦN VẼ BIỂU ĐỒ BẰNG MATPLOTLIB
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Vẽ đường cho Lazy Loading (Màu đỏ, điểm tròn)
plt.plot(author_limits, lazy_times, marker='o', color='red', linewidth=2, label='Lazy Loading (N+1 Problem)')

# Vẽ đường cho Eager Loading (Màu xanh dương, điểm vuông)
plt.plot(author_limits, eager_times, marker='s', color='blue', linewidth=2, label='Eager Loading (Batch/In-memory)')

# Cấu hình thông tin biểu đồ
plt.title('Impact of Network Latency (50ms) on Distributed ORM Loading Strategies', fontsize=14, fontweight='bold')
plt.xlabel('Number of Authors Queried', fontsize=12)
plt.ylabel('Execution Time (milliseconds)', fontsize=12)

# Bật lưới và hiển thị chú thích
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)

# Lưu biểu đồ ra file ảnh để đưa vào báo cáo
plt.savefig('n_plus_1_problem_chart.png', dpi=300, bbox_inches='tight')
print(" Đã lưu biểu đồ thành công: n_plus_1_problem_chart.png")

# Hiển thị biểu đồ lên màn hình
plt.show()