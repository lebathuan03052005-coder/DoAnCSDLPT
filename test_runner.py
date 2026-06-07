import requests
import matplotlib.pyplot as plt
import sys

# Địa chỉ của Main Application (Client entry point)
MAIN_APP_URL = "http://localhost:5000"

# Các mốc số lượng Tác giả cần test
author_limits = [10, 30, 50, 100]

lazy_times = []
eager_times = []

print("Bắt đầu chạy kịch bản Test Phân Tán (Microservices Architecture)...\n" + "-"*50)

for limit in author_limits:
    print(f" Đang test với {limit} tác giả...")
    
    # ---------------------------------------------------------
    # 1. Test Lazy Loading (N+1)
    # ---------------------------------------------------------
    try:
        response_lazy = requests.get(f"{MAIN_APP_URL}/test/lazy?limit={limit}")
        
        if response_lazy.status_code == 503:
            print("\n[LỖI MẠNG] Book Service (Node B) không khả dụng! (NODE_B_OFFLINE)")
            sys.exit()
            
        res_lazy = response_lazy.json()
        lazy_time = res_lazy['execution_time_ms']
        lazy_times.append(lazy_time)
        print(f"   - Lazy Loading: {lazy_time} ms (Số lần gọi mạng liên Node: {res_lazy['network_calls']})")
        
    except requests.exceptions.ConnectionError:
        print("\n[LỖI] Không thể kết nối tới Main App (Site A). Hãy đảm bảo main_app.py đang chạy!")
        sys.exit()

    # ---------------------------------------------------------
    # 2. Test Eager Loading (Select-in)
    # ---------------------------------------------------------
    response_eager = requests.get(f"{MAIN_APP_URL}/test/eager?limit={limit}")
    
    res_eager = response_eager.json()
    eager_time = res_eager['execution_time_ms']
    eager_times.append(eager_time)
    print(f"   - Eager Loading: {eager_time} ms (Số lần gọi mạng liên Node: {res_eager['network_calls']})")
    print("-" * 50)

print("\nĐã hoàn tất đo lường! Đang vẽ biểu đồ so sánh hiệu năng...")

# ---------------------------------------------------------
# VẼ BIỂU ĐỒ SO SÁNH
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(author_limits, lazy_times, marker='o', color='red', linewidth=2, label='Lazy Loading (N+1 Overhead)')
plt.plot(author_limits, eager_times, marker='s', color='blue', linewidth=2, label='Eager Loading (Set-based Batching)')

plt.title('Performance Impact: Lazy vs Eager Loading in Microservices (Latency=50ms)', fontsize=14, fontweight='bold')
plt.xlabel('Number of Authors (N)', fontsize=12)
plt.ylabel('Total Execution Time (ms)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)

plt.savefig('n_plus_1_problem_chart.png', dpi=300, bbox_inches='tight')
print(" Đã lưu biểu đồ: n_plus_1_problem_chart.png")
plt.show()