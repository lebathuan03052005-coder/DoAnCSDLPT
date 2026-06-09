import requests
import matplotlib.pyplot as plt
import sys

# Main Application (Gateway)
MAIN_APP_URL = "http://localhost:5000"

# Các mốc số lượng Author
author_limits = [10, 30, 50, 100]

lazy_times = []
eager_times = []

print("Bắt đầu chạy kịch bản Test Phân Tán (Microservices Architecture)")
print("-" * 60)

for limit in author_limits:

    print(f"\nĐang test với {limit} tác giả")

    # ======================================================
    # 1. Lazy Loading
    # ======================================================
    try:
        response_lazy = requests.get(
            f"{MAIN_APP_URL}/test/lazy?limit={limit}"
        )

        if response_lazy.status_code == 503:
            print("Author Service không khả dụng!")
            sys.exit()

        res_lazy = response_lazy.json()

        lazy_time = res_lazy["execution_time_ms"]
        lazy_times.append(lazy_time)

        print(
            f"Lazy Loading : {lazy_time} ms "
            f"(Network calls = {res_lazy['network_calls']})"
        )

    except requests.exceptions.ConnectionError:
        print("Không thể kết nối tới Main App!")
        sys.exit()

    # ======================================================
    # 2. Eager Loading
    # ======================================================
    try:
        response_eager = requests.get(
            f"{MAIN_APP_URL}/test/eager?limit={limit}"
        )

        if response_eager.status_code == 503:
            print("Author Service không khả dụng!")
            sys.exit()

        res_eager = response_eager.json()

        eager_time = res_eager["execution_time_ms"]
        eager_times.append(eager_time)

        print(
            f"Eager Loading: {eager_time} ms "
            f"(Network calls = {res_eager['network_calls']})"
        )

    except requests.exceptions.ConnectionError:
        print("Không thể kết nối tới Main App!")
        sys.exit()

    print("-" * 60)

print("\nHoàn tất đo lường.")

# ======================================================
# Vẽ biểu đồ
# ======================================================
plt.figure(figsize=(10, 6))

plt.plot(
    author_limits,
    lazy_times,
    marker='o',
    color='red',
    linewidth=2,
    label='Lazy Loading (N+1)'
)

plt.plot(
    author_limits,
    eager_times,
    marker='s',
    color='blue',
    linewidth=2,
    label='Eager Loading (Batch Query)'
)

plt.title(
    'Performance Comparison: Lazy vs Eager Loading',
    fontsize=14,
    fontweight='bold'
)

plt.xlabel('Number of Authors')
plt.ylabel('Execution Time (ms)')

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.savefig(
    'n_plus_1_problem_chart.png',
    dpi=300,
    bbox_inches='tight'
)

print("Đã lưu biểu đồ: n_plus_1_problem_chart.png")

plt.show()