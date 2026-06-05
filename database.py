import time
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Cấu hình chuỗi kết nối 
DB_URI = "mssql+pyodbc://DESKTOP-03TS7J6/Authors_Book?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DB_URI, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 2. Cấu hình mô phỏng mạng
NETWORK_LATENCY = 0.05  # 50ms
network_metrics = {"calls": 0}  # Dùng dictionary để dễ dàng thay đổi giá trị từ file khác

def reset_network_calls():
    network_metrics["calls"] = 0

def get_network_calls():
    return network_metrics["calls"]

# Hook chặn mọi câu lệnh SQL để cộng dồn độ trễ
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    network_metrics["calls"] += 1
    time.sleep(NETWORK_LATENCY)